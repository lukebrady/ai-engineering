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
      Environment = var.environment
      ManagedBy   = "opentofu"
      Purpose     = "ai-inference-server"
    }
  }
}

# Data source for the latest Ubuntu 24.04 AI Inference AMI
data "aws_ami" "ai_inference" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["${var.ami_name_prefix}*"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# Security group for the AI inference server
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "ai_inference" {
  name_prefix = "ai-inference-"
  description = "Security group for AI inference server"
  vpc_id      = data.aws_vpc.default.id

  # SSH access
  ingress {
    description = "SSH from anywhere (consider restricting in production)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access (for web interfaces)
  ingress {
    description = "HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access
  ingress {
    description = "HTTPS access"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Custom ports for AI inference services
  dynamic "ingress" {
    for_each = var.additional_ports
    content {
      description = "Custom port ${ingress.value}"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ai-inference-security-group"
  }
}

# EC2 instance for AI inference
resource "aws_instance" "ai_inference_server" {
  ami                    = data.aws_ami.ai_inference.id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.ai_inference.id]
  subnet_id              = data.aws_subnets.default.ids[0]

  # EBS optimization for better performance
  ebs_optimized = true

  # Root block device configuration
  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name = "ai-inference-root-volume"
    }
  }

  # Additional EBS volumes for data and models
  dynamic "ebs_block_device" {
    for_each = var.additional_volumes
    content {
      device_name           = ebs_block_device.value.device_name
      volume_type           = ebs_block_device.value.volume_type
      volume_size           = ebs_block_device.value.volume_size
      encrypted             = true
      delete_on_termination = false

      tags = {
        Name = "ai-inference-${ebs_block_device.value.device_name}"
      }
    }
  }

  # User data script for instance initialization
  user_data = templatefile("${path.module}/user_data.sh", {
    environment  = var.environment
    project_name = "ai-inference"
  })

  # Instance metadata options for security
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "enabled"
  }

  # Monitoring and termination protection
  monitoring              = true
  disable_api_termination = var.disable_api_termination

  tags = {
    Name = "ai-inference-server"
  }

  # Lifecycle policy to prevent accidental replacement
  lifecycle {
    prevent_destroy = false # Set to true in production if needed
  }
}

# Elastic IP for the instance (optional)
resource "aws_eip" "ai_inference" {
  count    = var.create_eip ? 1 : 0
  instance = aws_instance.ai_inference_server.id
  domain   = "vpc"

  tags = {
    Name = "ai-inference-eip"
  }
}

# Outputs
output "instance_id" {
  description = "ID of the AI inference server instance"
  value       = aws_instance.ai_inference_server.id
}

output "public_ip" {
  description = "Public IP address of the AI inference server"
  value       = var.create_eip ? aws_eip.ai_inference[0].public_ip : aws_instance.ai_inference_server.public_ip
}

output "private_ip" {
  description = "Private IP address of the AI inference server"
  value       = aws_instance.ai_inference_server.private_ip
}

output "instance_arn" {
  description = "ARN of the AI inference server instance"
  value       = aws_instance.ai_inference_server.arn
}

output "ami_id" {
  description = "ID of the AMI used for the instance"
  value       = data.aws_ami.ai_inference.id
}

output "ami_name" {
  description = "Name of the AMI used for the instance"
  value       = data.aws_ami.ai_inference.name
}
