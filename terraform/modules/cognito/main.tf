variable "user_pool_name" { type = string }
variable "tags" { type = map(string), default = {} }

resource "aws_cognito_user_pool" "this" {
  name = var.user_pool_name
  auto_verified_attributes = ["email"]
  username_attributes = ["email"]
  schema = []
  tags = var.tags
}

resource "aws_cognito_user_pool_client" "app_client" {
  name = "${var.user_pool_name}-app-client"
  user_pool_id = aws_cognito_user_pool.this.id
  explicit_auth_flows = ["ALLOW_REFRESH_TOKEN_AUTH","ALLOW_USER_SRP_AUTH"]
}
