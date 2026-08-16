variable "dashboard_name" { type = string }
variable "widgets" { type = list(string), default = [] }

resource "aws_cloudwatch_dashboard" "this" {
  dashboard_name = var.dashboard_name
  dashboard_body = jsonencode({ widgets = var.widgets })
  depends_on = []
}
