# Variables for IAM role OpenTofu configuration

variable "aws_region" {
  description = "AWS region to deploy the AI inference server"
  type        = string
  default     = "us-east-1"
}
