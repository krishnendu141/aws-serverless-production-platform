# Environments and Promotion Strategy

TelcoFlow Nexus supports multiple deployment environments to enable safe development, testing, validation, and production release flows.

Environments

- test — Automated deploys from main (CI). Low-cost configuration, used for feature validation and automated integration tests.
- qa — Manual or gated deploys. Used by QA teams for integration testing, staging of longer-running scenarios.
- preprod — Near-production environment with production-like configuration (Aurora, higher retention, feature flags set to mirror prod). Requires approval to deploy.
- prod — Production environment. Strict controls, manual approvals, limited credentials and strong audit trails.

Best practices

1. Remote state and locking
   - Use an S3 backend for Terraform state and a DynamoDB table for state locking.
   - Each environment should use a separate state key (example: telcoflow-nexus/test/terraform.tfstate).

2. IAM & OIDC
   - Use GitHub OIDC for CI to assume short-lived roles per-environment.
   - Do NOT store long-lived AWS keys in GitHub Secrets.
   - Provide dedicated minimal roles per environment (TEST_DEPLOY_ROLE_ARN, QA_DEPLOY_ROLE_ARN, PREPROD_DEPLOY_ROLE_ARN, PROD_DEPLOY_ROLE_ARN).

3. Environment protection & approvals
   - Use GitHub Environments with required reviewers for qa/preprod/production.
   - Require manual approval or a small set of approvers for preprod and production pipeline runs.

4. Secrets management
   - Store secrets (DB credentials, Datadog keys, Bedrock credentials) in AWS Secrets Manager per environment.
   - Reference secrets from Terraform via data sources and provide them to Lambdas via environment variables or secure parameter store.

5. Branching & promotion workflow
   - Developers work on feature branches. Merge to main triggers test deployment.
   - QA or release engineers trigger QA workflow (manual dispatch) after test passes.
   - After QA signoff, trigger preprod deployment and post-validation, trigger prod deployment with manual approval.

6. Cost controls
   - In non-prod (test/qa), disable optional expensive services: Aurora, Datadog ingestion, Bedrock calls.
   - Use smaller retention for CloudWatch logs and lower read/write capacity planning in DynamoDB.
   - Use feature flags to gate expensive processing in lower environments.

7. Naming & tags
   - Tag every resource with consistent tags: Project=TelcoFlow-Nexus, Environment=<env>, ManagedBy=Terraform, Application=ServiceIntelligence, Owner=PlatformEngineering, CostCenter=Demo.
   - Use environment prefix in resource names to avoid cross-environment collisions (tf-nexus-<env>-resource).

8. Testing & CI
   - Unit tests run on every PR.
   - Integration tests should run in the test environment and be short-lived.
   - End-to-end smoke tests should run in preprod prior to production deployment.

9. Observability
   - Each environment should have its own CloudWatch dashboards and alarms with alerting channels assigned to on-call teams for that environment.
   - Production alerts should have stricter thresholds and separate notification routing than non-prod.

10. Disaster recovery & backups
   - Enable point-in-time recovery (PITR) for production DynamoDB tables and backup schedules for Aurora.
   - Use S3 versioning and lifecycle for audit exports.

11. Change control
   - All Terraform changes targeting prod must be peer-reviewed, accompanied by a runbook, and executed through the CI pipeline with approvals.


Example deployment commands

# Initialize and plan for test
cd terraform/environments/test
terraform init
terraform plan

# Apply for test
terraform apply

For QA/preprod/prod use the GitHub deployment workflows to ensure OIDC-based authentication and required approvals are enforced.
