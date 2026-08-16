variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_prefix" {
  type    = string
  default = "asp" # aws-serverless-production-platform
}

variable "artifacts_bucket_name" {
  type        = string
  description = "S3 bucket for artifacts and documents"
}

variable "chatbot_lambda_zip" {
  description = "Path to packaged chatbot lambda zip (local path)"
  type = string
  default = "../build/chatbot.zip"
}

variable "ingest_lambda_zip" {
  description = "Path to packaged ingest lambda zip (local path)"
  type = string
  default = "../build/ingest.zip"
}

variable "datadog_api_key" {
  description = "Datadog API Key (for Terraform provider)"
  type        = string
  default     = ""
}

variable "datadog_app_key" {
  description = "Datadog APP Key"
  type        = string
  default     = ""
}

variable "common_tags" {
  type = map(string)
  default = {
    Owner = "your-name"
    Project = "aws-serverless-production-platform"
  }
}
