# Backend and GitHub OIDC Setup

This document explains how to bootstrap the Terraform remote backend (S3 + DynamoDB) and how to configure GitHub Actions OIDC trust for safe deploys.

1) Bootstrap Terraform remote backend

Choose an S3 bucket name (global) and a DynamoDB table name for state locking.

Example:
  TF_STATE_BUCKET=tf-nexus-terraform-state
  TF_LOCKS_TABLE=tf-nexus-terraform-locks
  AWS_REGION=ap-south-1

Run the provided script (requires AWS CLI configured for the target account):

  ./scripts/bootstrap_tf_backend.sh $TF_STATE_BUCKET $TF_LOCKS_TABLE $AWS_REGION

Script actions:
- Creates S3 bucket (if not exists)
- Enables versioning and server-side encryption
- Creates DynamoDB table for state locking

2) Configure Terraform backend in each environment

In terraform/environments/<env>/main.tf uncomment and update the backend block with your bucket and lock table. Example:

terraform {
  backend "s3" {
    bucket = "tf-nexus-terraform-state"
    key    = "telcoflow-nexus/<env>/terraform.tfstate"
    region = "ap-south-1"
    dynamodb_table = "tf-nexus-terraform-locks"
  }
}

3) Configure GitHub OIDC provider in AWS

Create the OIDC provider (AWS CLI):

aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

(Thumbprint above is commonly used; validate for your environment.)

4) Create IAM roles for each environment with trust policy

Example trust policy (replace <account-id>, and restrict token.actions.githubusercontent.com:sub to your org/repo/branch):

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Federated": "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com" },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": { "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:ref:refs/heads/main" },
        "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" }
      }
    }
  ]
}

Create one role per environment (TEST_DEPLOY_ROLE, QA_DEPLOY_ROLE, PREPROD_DEPLOY_ROLE, PROD_DEPLOY_ROLE) and store the role ARNs in GitHub Secrets or Environment secrets.

5) Least-privilege policy for Terraform roles (example)

- s3:GetObject, s3:PutObject, s3:ListBucket on TF state bucket
- dynamodb:GetItem, PutItem, DeleteItem, UpdateItem on lock table
- sts:AssumeRole on roles that Terraform needs to pass/assume
- Resource scoped permissions for services created by Terraform (S3, Lambda, SQS, DynamoDB, etc.)

Example inline permit (replace placeholders):

{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:GetObject","s3:PutObject","s3:ListBucket"], "Resource": ["arn:aws:s3:::<TF_STATE_BUCKET>","arn:aws:s3:::<TF_STATE_BUCKET>/*"] },
    { "Effect": "Allow", "Action": ["dynamodb:GetItem","dynamodb:PutItem","dynamodb:DeleteItem","dynamodb:UpdateItem"], "Resource": ["arn:aws:dynamodb:<region>:<account-id>:table/<TF_LOCKS_TABLE>"] },
    { "Effect": "Allow", "Action": ["sts:AssumeRole"], "Resource": ["arn:aws:iam::<account-id>:role/tf-nexus-*" ] }
  ]
}

6) Configure GitHub workflows to use OIDC

In workflow YAML add:

permissions:
  id-token: write
  contents: read

Then use the configure-aws-credentials action:

- name: Configure AWS Credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v2
  with:
    role-to-assume: ${{ secrets.TEST_DEPLOY_ROLE_ARN }}
    aws-region: ap-south-1

7) Security checklist before production

- Ensure roles are tightly scoped to the repository and branch
- Require GitHub Environment approvals and reviewers for preprod/prod
- Audit CloudTrail for AssumeRole events
- Rotate any secrets and avoid storing AWS keys in GitHub

Further help

If you want, I can generate the exact AWS CLI commands and IAM role JSON files for each environment (test/qa/preprod/prod) and add them to scripts/ for copy-paste deployment.
