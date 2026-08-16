# AWS Serverless Production Platform

This project contains a production-ready scaffold for an AWS Serverless platform with RAG chatbot integration (Bedrock), Step Functions, Lambda, SQS/SNS, S3, API Gateway, least-privilege IAM, Datadog observability, and GitHub Actions CI/CD using OIDC.

This scaffold is safe to review locally. It contains Terraform IaC to create the resources and Python Lambda handlers with local-mode stubs. You must provide AWS and Datadog configuration to deploy for real.

Directory layout
- infra/: Terraform code
- src/: Python Lambda handlers
- sfn/: Step Functions state machine definition
- .github/workflows/: CI/CD workflows (OIDC deploy)
- observability/: Datadog dashboard and alerts
- docs/: usage and architecture notes
- architecture-diagrams/: mermaid diagram

See docs/USAGE.md for quick start and deployment notes.
