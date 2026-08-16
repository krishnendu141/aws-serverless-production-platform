GitHub OIDC and IAM Roles for TelcoFlow Nexus

Purpose

Use GitHub Actions OIDC provider to allow CI pipelines to assume short-lived IAM roles per environment. This avoids long-lived AWS credentials in GitHub Secrets and enables least-privilege ephemeral access.

Overview

- Create an IAM OIDC identity provider for GitHub in the AWS account.
- Create one IAM role per environment (test, qa, preprod, prod) with a trust policy allowing the GitHub OIDC provider and specific repository "sub" condition and audience (sts.amazonaws.com).
- Attach least-privilege policy to the role with only the permissions needed for Terraform runs and deployments.

Example: Create OIDC provider (AWS CLI)

aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list <thumbprint>

Example trust policy for a role (replace <account-id> and repo)

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

Least-privilege policy example for Terraform runs (plan/apply for environment)

- s3:GetObject, s3:PutObject, s3:ListBucket for terraform backend bucket
- dynamodb:GetItem, PutItem, DeleteItem, UpdateItem for lock table
- iam:PassRole for roles created by terraform (if needed)
- ec2/VPC operations (if creating NAT, ENIs), lambda, sqs, s3, dynamodb permissions scoped to resource ARNs for the environment

Example inline policy (replace placeholders)

{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:GetObject","s3:PutObject","s3:ListBucket"], "Resource": ["arn:aws:s3:::<tf-state-bucket>","arn:aws:s3:::<tf-state-bucket>/*"] },
    { "Effect": "Allow", "Action": ["dynamodb:GetItem","dynamodb:PutItem","dynamodb:DeleteItem","dynamodb:UpdateItem"], "Resource": ["arn:aws:dynamodb:<region>:<account-id>:table/<tf-locks-table>"] },
    { "Effect": "Allow", "Action": ["sts:AssumeRole"], "Resource": ["arn:aws:iam::<account-id>:role/tf-nexus-*" ] }
  ]
}

Notes

- Use GitHub repository-level conditions to restrict which repo/branch can assume which environment role.
- Use GitHub Environments to store small secrets (like role ARNs) and to require reviewers for production deploys.
- Do not attach overly broad policies to the OIDC role. Limit to necessary actions and resource ARNs.

Steps to enable OIDC in GitHub Actions workflow

- In the workflow, use aws-actions/configure-aws-credentials@v2 with role-to-assume set to the environment role ARN.
- Ensure the workflow identity token is requested (id-token: write permissions in workflow).

Example step

- name: Configure AWS Credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v2
  with:
    role-to-assume: ${{ secrets.QA_DEPLOY_ROLE_ARN }}
    aws-region: ap-south-1

Security checklist

- Verify the OIDC provider thumbprint and repository conditions
- Require MFA for role creation/changes
- Audit CloudTrail for sts:AssumeRole operations from GitHub OIDC
