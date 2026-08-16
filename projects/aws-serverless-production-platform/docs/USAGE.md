# AWS Serverless Production Platform - Usage

This document explains how to get started with the project locally and how to deploy safely.

Prerequisites
- Terraform >= 1.0
- AWS CLI configured (for local testing) or GitHub OIDC role set (recommended)
- Python 3.10
- Optional: Datadog account & API keys to enable dashboards and monitors

Quick local steps (no infra changes):
1. Review code under projects/aws-serverless-production-platform/src
2. Package lambdas (locally):
   bash projects/aws-serverless-production-platform/build/package-lambdas.sh

Deploy using GitHub Actions (recommended):
- Create an IAM role for GitHub OIDC with a trust policy and least-privilege permissions for terraform apply and lambda updates.
- Set the following repository secrets:
  - AWS_OIDC_ROLE_ARN: arn:aws:iam::123456789012:role/your-github-oidc-role
  - AWS_ACCOUNT_ID: 123456789012
  - DATADOG_API_KEY, DATADOG_APP_KEY (optional for dashboard)

Then go to Actions -> Deploy to AWS (OIDC) and trigger the workflow.

Notes
- Terraform references local zip paths by default. The deploy workflow packages lambdas; ensure S3 upload or adjust terraform to use local_file & aws_lambda_function filename paths as desired.
- Bedrock integration in lambda is mocked if Bedrock isn't available in your account; replace model invocation with real modelId and payload according to Bedrock API.
