# Runbook: DLQ Recovery

Symptoms

- DLQ message count rising
- Messages indicate downstream errors or malformed payloads

Investigation

1. Inspect DLQ via AWS Console or SQS API
2. Sample messages and check failure_reason

Remediation

- For retryable errors: re-enqueue to the original queue after correction
- For malformed payloads: quarantine and open manual review

Commands

aws sqs receive-message --queue-url <dlq-url> --max-number-of-messages 10

Post-incident

- Increase visibility timeout if consumers are failing due to timeouts
- Tune retry and backoff policies
