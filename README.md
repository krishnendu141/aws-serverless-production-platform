# TelcoFlow Nexus

Enterprise Event-Driven Telecom Service Request Intelligence Platform

Overview

TelcoFlow Nexus ingests, classifies, enriches and routes customer service requests at enterprise scale using AWS managed services and Terraform. The platform supports multiple environments (test, qa, preprod, prod) with best-practice CI/CD, remote state, and approval gates.

Quick links

- Environments: terraform/environments/{test,qa,preprod,prod}
- Core lambdas: src/lambdas/
- Docs: docs/
- Examples: examples/requests/

Environments

This repository includes environment-specific Terraform workspaces for:
- test (automated deploys)
- qa (gated)
- preprod (near-prod validation)
- prod (manual approval)

See docs/ENVIRONMENTS.md for recommended practices and required CI/OIDC setup.

Getting started (developer)

1. Install dependencies: make install
2. Run unit tests: make test
3. Initialize Terraform for test: cd terraform/environments/test && terraform init
4. Plan and apply in test (ensure backend is configured): terraform plan && terraform apply

Contributing

See CONTRIBUTING.md for repo standards.

License

MIT
