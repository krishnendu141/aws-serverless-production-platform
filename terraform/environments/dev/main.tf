terraform {
  required_version = ">= 1.2"
}

provider "aws" {
  region = var.region
}

module "network" {
  source = "../../modules/network"
  cidr = "10.0.0.0/16"
  azs = ["ap-south-1a","ap-south-1b"]
  public_subnet_cidrs = ["10.0.1.0/24","10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.101.0/24","10.0.102.0/24"]
  tags = local.common_tags
}

locals {
  common_tags = {
    Project = "TelcoFlow-Nexus"
    Environment = "dev"
    ManagedBy = "Terraform"
    Application = "ServiceIntelligence"
    Owner = "PlatformEngineering"
    CostCenter = "Demo"
  }
}

output "api_url" {
  value = "https://api.example.com"
}
