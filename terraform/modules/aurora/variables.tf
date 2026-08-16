variable "db_cluster_identifier" { type = string }
variable "engine" { type = string, default = "aurora-postgresql" }
variable "engine_version" { type = string, default = "13.6" }
variable "instance_class" { type = string, default = "db.serverless" }
variable "subnet_ids" { type = list(string) }
variable "vpc_security_group_ids" { type = list(string), default = [] }
variable "tags" { type = map(string), default = {} }
