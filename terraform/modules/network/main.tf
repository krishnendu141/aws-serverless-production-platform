// Terraform network module for TelcoFlow Nexus
// Creates VPC, subnets, route tables and NAT gateway (minimal skeleton). Fill variables in module usage.

variable "cidr" { type = string }
variable "azs" { type = list(string) }
variable "public_subnet_cidrs" { type = list(string) }
variable "private_subnet_cidrs" { type = list(string) }
variable "tags" { type = map(string) }

resource "aws_vpc" "this" {
  cidr_block = var.cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = merge(var.tags, { Name = "tf-nexus-vpc" })
}

// Additional resources (subnets, route tables, IGW, NAT) to be implemented per environment
