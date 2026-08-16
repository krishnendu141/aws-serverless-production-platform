terraform {
  required_version = ">= 1.2"
}

provider "aws" {
  region = var.region
}

module "network" {
  source = "../../modules/network"
  cidr = "10.2.0.0/16"
  azs = ["ap-south-1a","ap-south-1b","ap-south-1c"]
  public_subnet_cidrs = ["10.2.1.0/24","10.2.2.0/24","10.2.3.0/24"]
  private_subnet_cidrs = ["10.2.101.0/24","10.2.102.0/24","10.2.103.0/24"]
  tags = local.common_tags
}

locals {
  common_tags = {
    Project = "TelcoFlow-Nexus"
    Environment = var.environment
    ManagedBy = "Terraform"
    Application = "ServiceIntelligence"
    Owner = "PlatformEngineering"
    CostCenter = "Demo"
  }
}

module "kms" {
  source = "../../modules/kms"
  alias = "alias/tf-nexus-${var.environment}-kms"
  tags = local.common_tags
}

module "s3_logs" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-logs"
  tags = local.common_tags
  lifecycle_rules = []
}

module "dynamodb_idempotency" {
  source = "../../modules/dynamodb"
  name = "tf-nexus-${var.environment}-idempotency"
  hash_key = "event_id"
  tags = local.common_tags
}

module "eventbus" {
  source = "../../modules/eventbridge"
  name = "telcoflow-nexus-${var.environment}-events"
  tags = local.common_tags
}

module "sqs_ingress" {
  source = "../../modules/sqs"
  name = "tf-nexus-${var.environment}-ingress-request-queue"
  tags = local.common_tags
}

module "iam_lambda_role" {
  source = "../../modules/iam"
  name = "tf-nexus-${var.environment}-lambda-role"
  assume_service = "lambda.amazonaws.com"
}

module "s3_raw" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-raw-requests"
  tags = local.common_tags
  lifecycle_rules = [ { id = "raw-expire", enabled = true, prefix = "raw/", days = 365 } ]
}

module "s3_attachments" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-attachments"
  tags = local.common_tags
  lifecycle_rules = [ { id = "attachments-archive", enabled = true, prefix = "attachments/", days = 90 } ]
}

module "s3_processed" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-processed"
  tags = local.common_tags
}

module "s3_audit" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-audit-exports"
  tags = local.common_tags
  lifecycle_rules = [ { id = "audit-tiers", enabled = true, prefix = "", days = 365 } ]
}

module "s3_failed" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-failed-payloads"
  tags = local.common_tags
}

module "s3_analytics" {
  source = "../../modules/s3"
  name = "tf-nexus-${var.environment}-analytics-exports"
  tags = local.common_tags
}

# Backend configuration should be provided per-organization with secure S3 bucket and DynamoDB lock table.
# Example backend (commented):
# terraform {
#   backend "s3" {
#     bucket = "<tf-state-bucket>"
#     key    = "telcoflow-nexus/preprod/terraform.tfstate"
#     region = var.region
#     dynamodb_table = "<tf-locks-table>"
#   }
# }
