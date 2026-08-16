# ADR 001 — Event-driven architecture

Date: 2026-08-17

Status: Accepted

Context

TelcoFlow Nexus must process high volumes of asynchronous customer service requests originating from multiple channels. The platform should be scalable, decoupled, and resilient to partial failures.

Decision

Adopt an event-driven architecture built with SQS for buffering and backpressure, EventBridge for domain event fanout, and Step Functions for orchestration. Lambda functions implement single responsibilities.

Consequences

- Good decoupling and horizontal scalability
- Need to implement idempotency and monitoring
- Operational complexity increased but manageable
