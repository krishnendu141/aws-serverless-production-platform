variable "name" { type = string }
variable "tags" { type = map(string) }
variable "redrive_policy" { type = map(any), default = {} }
