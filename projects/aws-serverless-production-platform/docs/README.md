# Project: AWS Serverless Production Platform

This repository contains a production-ready scaffold to demonstrate serverless architecture on AWS, focusing on:
- Serverless compute (AWS Lambda)
- Orchestration (AWS Step Functions)
- Messaging (SQS / SNS)
- Storage (S3)
- API surface (API Gateway)
- RAG chatbot orchestration (Bedrock integration)
- Observability (Datadog + CloudWatch)
- CI/CD (GitHub Actions with OIDC)

Key files
- infra/: Terraform configuration
- src/: Lambda source code
- sfn/state_machine.json: Step Functions definition
- observability/: Datadog dashboards
- .github/workflows/: CI / Deploy
- docs/USAGE.md: How to deploy and use

This scaffold is opinionated for clarity and safety. Before running terraform apply, fill in the required variables and ensure IAM roles for GitHub OIDC are in place.
