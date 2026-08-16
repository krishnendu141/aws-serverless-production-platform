variable "alias" { type = string }
variable "description" { type = string, default = "KMS key for TelcoFlow Nexus" }
variable "tags" { type = map(string), default = {} }

resource "aws_kms_key" "this" {
  description = var.description
  deletion_window_in_days = 30
  tags = var.tags
}

resource "aws_kms_alias" "this" {
  name = var.alias
  target_key_id = aws_kms_key.this.key_id
}
