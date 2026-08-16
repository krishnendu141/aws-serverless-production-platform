variable "alias" { type = string }
variable "description" { type = string, default = "KMS key for TelcoFlow Nexus" }
variable "tags" { type = map(string), default = {} }
