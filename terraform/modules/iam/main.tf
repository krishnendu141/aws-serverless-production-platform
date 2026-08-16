variable "name" { type = string }
variable "assume_service" { type = string }
variable "inline_policies" { type = map(string), default = {} }

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals { type = "Service" , identifiers = [var.assume_service] }
  }
}

resource "aws_iam_role" "this" {
  name = var.name
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

# Create inline role policies when provided via the inline_policies map
resource "aws_iam_role_policy" "inline" {
  for_each = var.inline_policies
  name     = each.key
  role     = aws_iam_role.this.name
  policy   = each.value
}

output "role_arn" { value = aws_iam_role.this.arn }
output "role_name" { value = aws_iam_role.this.name }
