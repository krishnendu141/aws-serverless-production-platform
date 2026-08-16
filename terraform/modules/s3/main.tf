variable "name" { type = string }
variable "tags" { type = map(string) }
variable "lifecycle_rules" { type = list(object({ id = string, enabled = bool, prefix = string, days = number })) , default = [] }

resource "aws_s3_bucket" "this" {
  bucket = var.name
  acl    = "private"
  versioning { enabled = true }
  server_side_encryption_configuration {
    rule { apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" } }
  }
  tags = var.tags
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "deny_insecure_transport" {
  bucket = aws_s3_bucket.this.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid = "DenyInsecureTransport",
        Effect = "Deny",
        Principal = "*",
        Action = "s3:*",
        Resource = [aws_s3_bucket.this.arn, "${aws_s3_bucket.this.arn}/*"],
        Condition = { Bool = { "aws:SecureTransport" = false } }
      }
    ]
  })
}

# lifecycle rules (optional)
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id      = rule.value.id
      enabled = rule.value.enabled
      prefix  = rule.value.prefix
      expiration { days = rule.value.days }
    }
  }
}
