// Lambda module skeleton: deploy a function with IAM role, environment and optional VPC config
variable "function_name" { type = string }
variable "handler" { type = string }
variable "runtime" { type = string, default = "python3.10" }
variable "memory_size" { type = number, default = 512 }
variable "timeout" { type = number, default = 30 }
variable "environment" { type = map(string), default = {} }
variable "tags" { type = map(string) }

resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
  statement { actions = ["sts:AssumeRole"] principals { type = "Service" identifiers = ["lambda.amazonaws.com"] } }
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  filename = "placeholder.zip" // packaging handled externally
  handler = var.handler
  runtime = var.runtime
  role = aws_iam_role.lambda_role.arn
  memory_size = var.memory_size
  timeout = var.timeout
  environment { variables = var.environment }
  tags = var.tags
}
