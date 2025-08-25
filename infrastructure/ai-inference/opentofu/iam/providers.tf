# OpenTofu configuration for AI Inference Server
# This configuration creates an L4 instance using the custom AMI

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# AWS Provider configuration
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ai-inference"
      ManagedBy   = "opentofu"
      Purpose     = "ai-inference"
    }
  }
}
