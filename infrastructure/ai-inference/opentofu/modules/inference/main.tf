# Resources for AI Inference Server
# This configuration creates an L4 instance using the custom AMI

# Generate SSH key pair locally
resource "tls_private_key" "this" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create AWS key pair from the generated public key
resource "aws_key_pair" "this" {
  key_name   = var.key_name
  public_key = tls_private_key.this.public_key_openssh

  tags = {
    Name = var.key_name
  }
}

# Save private key to local file (for local development only)
resource "local_file" "private_key" {
  content         = tls_private_key.this.private_key_pem
  filename        = "${path.module}/${var.key_name}.pem"
  file_permission = "0600"
}

# Security group for the AI inference server
resource "aws_security_group" "this" {
  name_prefix = "ai-inference-"
  description = "Security group for AI inference server"
  vpc_id      = var.vpc_id

  # SSH access - only from allowed IPs
  dynamic "ingress" {
    for_each = length(var.allowed_ip_addresses) > 0 ? [1] : []
    content {
      description = "SSH access from allowed IPs"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = var.allowed_ip_addresses
    }
  }

  # HTTPS access - only from allowed IPs
  dynamic "ingress" {
    for_each = length(var.allowed_ip_addresses) > 0 ? [1] : []
    content {
      description = "HTTPS access from allowed IPs"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = var.allowed_ip_addresses
    }
  }

  # Custom ports for AI inference services - only from allowed IPs
  dynamic "ingress" {
    for_each = length(var.allowed_ip_addresses) > 0 ? var.additional_ports : []
    content {
      description = "Custom port ${ingress.value} from allowed IPs"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = var.allowed_ip_addresses
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
resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.this.key_name
  vpc_security_group_ids = [aws_security_group.this.id]
  subnet_id              = var.subnet_id
  iam_instance_profile   = var.iam_instance_profile

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

  # User data script for instance initialization
  user_data = templatefile("${path.module}/scripts/user_data.sh", {
    hugging_face_token = var.hugging_face_token
    model              = var.model
    vllm_args          = var.vllm_args
    vllm_timeout       = var.vllm_timeout
    vllm_version       = var.vllm_version
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
}

# Elastic IP for the instance (optional)
resource "aws_eip" "this" {
  count    = var.create_eip ? 1 : 0
  instance = aws_instance.this.id
  domain   = "vpc"

  tags = {
    Name = "ai-inference-eip"
  }
}

