variable "name" { type = string }
variable "tags" { type = map(string) }

resource "aws_cloudwatch_event_bus" "this" {
  name = var.name
  tags = var.tags
}

# Consumers and rules should be added by environment-specific code using aws_cloudwatch_event_rule and targets
