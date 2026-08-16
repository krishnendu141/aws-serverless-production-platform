variable "name" { type = string }
variable "tags" { type = map(string) }
variable "redrive_policy" { type = map(any), default = {} }

resource "aws_sqs_queue" "this" {
  name                      = var.name
  visibility_timeout_seconds = 60
  message_retention_seconds  = 1209600
  receive_wait_time_seconds  = 20
  kms_master_key_id          = "alias/aws/sqs"
  tags = var.tags
  dynamic "redrive_policy" {
    for_each = length(keys(var.redrive_policy)) > 0 ? [var.redrive_policy] : []
    content { dead_letter_target_arn = redrive_policy.value.dead_letter_target_arn, max_receive_count = redrive_policy.value.max_receive_count }
  }
}

resource "aws_sqs_queue" "dlq" {
  count = contains(var.name, "-dlq") ? 0 : 0
  name  = "${var.name}-dlq"
  kms_master_key_id = "alias/aws/sqs"
  tags = var.tags
}
