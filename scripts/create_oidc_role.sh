#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/create_oidc_role.sh <role-name> <account-id> <repo> <branch>
ROLE_NAME=${1:-}
ACCOUNT_ID=${2:-}
REPO=${3:-}
BRANCH=${4:-main}

if [ -z "$ROLE_NAME" ] || [ -z "$ACCOUNT_ID" ] || [ -z "$REPO" ]; then
  echo "Usage: $0 <role-name> <account-id> <repo> <branch>"
  exit 1
fi

TRUST_POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com" },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": { "token.actions.githubusercontent.com:sub": "repo:${REPO}:ref:refs/heads/${BRANCH}" },
        "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" }
      }
    }
  ]
}
EOF
)

echo "$TRUST_POLICY" > /tmp/${ROLE_NAME}-trust.json
aws iam create-role --role-name "$ROLE_NAME" --assume-role-policy-document file:///tmp/${ROLE_NAME}-trust.json || true

echo "Created role $ROLE_NAME (or already exists). Attach policies as needed."
