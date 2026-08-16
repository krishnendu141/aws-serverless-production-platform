# Failure Handling

This document outlines how TelcoFlow Nexus handles common failure scenarios.

Key principles

- Design for at-least-once delivery and idempotency
- Use SQS DLQs, Step Functions retry/Catch, and Lambda retry strategies
- Implement poison message detection and quarantine
- Provide operational runbooks for common failures

Examples

- Lambda failure: CloudWatch alarm -> Investigate logs -> Retry or rollback
- DLQ messages: Use dlq_reprocessor to classify retryable messages and re-enqueue
- Bedrock unavailable: fall back to deterministic classification
- DynamoDB throttling: exponential backoff + provisioned increases or on-demand switch
