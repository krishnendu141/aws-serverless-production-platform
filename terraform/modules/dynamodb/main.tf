variable "name" { type = string }
variable "hash_key" { type = string }
variable "range_key" { type = string, default = "" }
variable "tags" { type = map(string) }

resource "aws_dynamodb_table" "this" {
  name         = var.name
  hash_key     = var.hash_key
  billing_mode = "PAY_PER_REQUEST"

  dynamic "attribute" {
    for_each = var.range_key != "" ? [var.range_key] : []
    content { name = var.range_key, type = "S" }
  }

  attribute {
    name = var.hash_key
    type = "S"
  }

  point_in_time_recovery { enabled = true }
  ttl { attribute_name = "expires_at" , enabled = true }
  server_side_encryption { enabled = true }
  tags = var.tags
}
