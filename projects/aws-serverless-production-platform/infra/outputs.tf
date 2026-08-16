output "chatbot_lambda_name" {
  value = aws_lambda_function.chatbot.function_name
}

output "ingest_lambda_name" {
  value = aws_lambda_function.ingest.function_name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.work_queue.id
}

output "s3_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}
