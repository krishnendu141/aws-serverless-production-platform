terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    datadog = {
      source  = "DataDog/datadog"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
}

# S3 bucket for artifacts and RAG documents
resource "aws_s3_bucket" "artifacts" {
  bucket = var.artifacts_bucket_name
  acl    = "private"
  tags = var.common_tags
}

# SNS topic for notifications
resource "aws_sns_topic" "platform_notifications" {
  name = "${var.project_prefix}-notifications"
  tags = var.common_tags
}

# SQS queue for async processing
resource "aws_sqs_queue" "work_queue" {
  name                      = "${var.project_prefix}-work-queue"
  visibility_timeout_seconds = 30
  message_retention_seconds  = 86400
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
  tags = var.common_tags
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.project_prefix}-dlq"
  tags = var.common_tags
}

# IAM role for Lambda execution (least privilege)
resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_prefix}-lambda-exec"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Inline policy granting minimal access to S3, SQS, SNS, Step Functions and Bedrock (bedrock actions require AWS-managed policy when available)
resource "aws_iam_policy" "lambda_inline_policy" {
  name        = "${var.project_prefix}-lambda-inline"
  description = "Least-privilege policy for platform lambdas"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        Resource = aws_sqs_queue.work_queue.arn
      },
      {
        Effect = "Allow",
        Action = ["sns:Publish"],
        Resource = aws_sns_topic.platform_notifications.arn
      },
      {
        Effect = "Allow",
        Action = ["states:StartExecution","states:DescribeExecution"],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_inline_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_inline_policy.arn
}

# Lambda functions (package and deploy separately)
# We create lambda function resource with placeholders so terraform plan will show expected changes.
resource "aws_lambda_function" "chatbot" {
  filename         = var.chatbot_lambda_zip      # path to zip produced by build
  function_name    = "${var.project_prefix}-chatbot"
  handler          = "app.handler"
  runtime          = "python3.10"
  role             = aws_iam_role.lambda_exec.arn
  source_code_hash = filebase64sha256(var.chatbot_lambda_zip)
  environment {
    variables = {
      ARTIFACTS_BUCKET = aws_s3_bucket.artifacts.bucket
      SQS_QUEUE_URL    = aws_sqs_queue.work_queue.id
      DATADOG_API_KEY  = var.datadog_api_key
    }
  }
  tags = var.common_tags
}

resource "aws_lambda_function" "ingest" {
  filename         = var.ingest_lambda_zip
  function_name    = "${var.project_prefix}-ingest"
  handler          = "ingest.handler"
  runtime          = "python3.10"
  role             = aws_iam_role.lambda_exec.arn
  source_code_hash = filebase64sha256(var.ingest_lambda_zip)
  environment {
    variables = {
      ARTIFACTS_BUCKET = aws_s3_bucket.artifacts.bucket
    }
  }
  tags = var.common_tags
}

# Step Functions state machine
resource "aws_sfn_state_machine" "platform_sfn" {
  name     = "${var.project_prefix}-state-machine"
  role_arn = aws_iam_role.sfn_role.arn
  definition = file("${path.module}/../sfn/state_machine.json")
  tags = var.common_tags
}

resource "aws_iam_role" "sfn_role" {
  name = "${var.project_prefix}-sfn-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "states.amazonaws.com" },
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_role_policy" "sfn_policy" {
  role = aws_iam_role.sfn_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction",
          "sqs:SendMessage"
        ],
        Resource = "*"
      }
    ]
  })
}

# API Gateway (REST) -> Lambda integration (minimal)
resource "aws_api_gateway_rest_api" "api" {
  name = "${var.project_prefix}-api"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  tags = var.common_tags
}

resource "aws_api_gateway_resource" "chat" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "chat"
}

resource "aws_api_gateway_method" "post_chat" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.chat.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_chat_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.chat.id
  http_method = aws_api_gateway_method.post_chat.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri  = aws_lambda_function.chatbot.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chatbot.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

# Datadog dashboard example
resource "datadog_dashboard" "platform_dashboard" {
  title       = "Platform Overview"
  description = "Overview dashboard for Serverless Production Platform"
  layout_type = "ordered"
  is_read_only = false
  widgets = jsonencode([
    {
      "definition" = {
        "type" = "timeseries",
        "requests" = [
          {
            "q" = "avg:aws.lambda.duration{functionname:${aws_lambda_function.chatbot.function_name}}"
          }
        ],
        "title" = "Chatbot Lambda duration"
      }
    }
  ])
}

# Outputs
output "api_invoke_url" {
  description = "Base API invoke URL"
  value = "${aws_api_gateway_rest_api.api.execution_arn}"
}
