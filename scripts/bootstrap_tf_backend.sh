#!/usr/bin/env bash
set -euo pipefail

# Bootstrap Terraform remote state backend: S3 bucket and DynamoDB lock table
# Usage: ./scripts/bootstrap_tf_backend.sh <s3-bucket-name> <dynamodb-table-name> <aws-region>

BUCKET=${1:-}
LOCK_TABLE=${2:-}
REGION=${3:-ap-south-1}

if [ -z "$BUCKET" ] || [ -z "$LOCK_TABLE" ]; then
  echo "Usage: $0 <tf-state-bucket> <tf-locks-table> [region]"
  exit 1
fi

echo "Creating S3 bucket: $BUCKET in $REGION"
aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" --create-bucket-configuration LocationConstraint=$REGION || true

echo "Enabling versioning and encryption"
aws s3api put-bucket-versioning --bucket "$BUCKET" --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket "$BUCKET" --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

echo "Creating DynamoDB lock table: $LOCK_TABLE"
aws dynamodb create-table --table-name "$LOCK_TABLE" --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region "$REGION" || true

echo "Waiting for lock table to become active"
aws dynamodb wait table-exists --table-name "$LOCK_TABLE" --region "$REGION"

echo "Backend bootstrap complete. Update terraform/environments/* main.tf backend blocks to use bucket $BUCKET and table $LOCK_TABLE"
