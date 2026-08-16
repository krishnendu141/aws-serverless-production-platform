variable "enable" { type = bool, default = false }
variable "api_key_ssm_path" { type = string, default = "" }
variable "tags" { type = map(string), default = {} }

# Datadog integration should be conditional and use secure API keys from SSM/Secrets Manager.
# This module is a placeholder for configuring Datadog Lambda layers, subscriptions and forwarders.
