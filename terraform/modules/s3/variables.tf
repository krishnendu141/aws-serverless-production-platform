variable "name" { type = string }
variable "tags" { type = map(string) }
variable "lifecycle_rules" { type = list(object({ id = string, enabled = bool, prefix = string, days = number })) , default = [] }
