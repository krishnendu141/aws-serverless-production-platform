# COST_ESTIMATION (Development Environment)

Estimated monthly cost (very approximate) for a small dev deployment:

- Lambda (20 functions, low traffic): $10 - $50
- API Gateway: $5 - $20
- SQS (several queues): $5 - $15
- EventBridge: $2 - $10
- Step Functions: $10 - $30
- DynamoDB (on-demand small tables): $20 - $100
- S3 (small usage): $1 - $5
- CloudWatch Logs & Metrics: $10 - $50
- NAT Gateway: $70 (single) — avoid in dev or use VPC endpoints
- Aurora Serverless (optional): $50 - $200 (depends on usage)
- Bedrock usage: billed per-invocation — optional and can be expensive

To reduce costs in dev:
- Disable Bedrock and Datadog
- Use on-demand DynamoDB and small retention for logs
- Use no NAT Gateway by avoiding Lambda in private subnets unless necessary

