# Variables for AI Inference Server OpenTofu configuration

variable "aws_region" {
  description = "AWS region to deploy the AI inference server"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "ami_name_prefix" {
  description = "Prefix for the AMI name to search for"
  type        = string
  default     = "ubuntu-24.04-ai-inference"
}

variable "allowed_ip_addresses" {
  description = "List of IP addresses (CIDR blocks) allowed to access the server"
  type        = list(string)
  default     = [] # Empty list by default - user must specify IPs for security
}

variable "hugging_face_token" {
  description = "Hugging Face token"
  type        = string
  sensitive   = true
}

variable "model" {
  description = "Model to use for inference"
  type        = string
  default     = "Qwen/Qwen3-0.6B"
}
