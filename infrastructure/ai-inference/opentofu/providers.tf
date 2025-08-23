# OpenTofu configuration for AI Inference Server
# This configuration creates an L4 instance using the custom AMI

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# AWS Provider configuration
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ai-inference"
      Environment = var.environment
      ManagedBy   = "opentofu"
      Purpose     = "ai-inference-server"
    }
  }
}
