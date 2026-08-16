# Simple build script to package lambdas into zips for Terraform deployment

set -e

mkdir -p build

pushd src/lambda_chatbot
zip -r ../../projects/aws-serverless-production-platform/build/chatbot.zip .
popd

pushd src/lambda_ingest
zip -r ../../projects/aws-serverless-production-platform/build/ingest.zip .
popd

pushd src/lambda_worker
zip -r ../../projects/aws-serverless-production-platform/build/worker.zip .
popd
