# Packer variables for Ubuntu 24.04 AI Inference AMI
# Override these values as needed for your environment

variable "aws_region" {
  type        = string
  description = "AWS region to build the AMI in"
  default     = "us-east-1"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type to use for building"
  default     = "t3.medium"
}

variable "ami_name_prefix" {
  type        = string
  description = "Prefix for the AMI name"
  default     = "ubuntu-24.04-ai-inference"
}

variable "ami_description" {
  type        = string
  description = "Description for the AMI"
  default     = "Ubuntu 24.04 AMI for AI inference workloads"
}

variable "ssh_username" {
  type        = string
  description = "SSH username for the base image"
  default     = "ubuntu"
}

variable "volume_size" {
  type        = number
  description = "Size of the EBS volume in GB"
  default     = 20
}

variable "volume_type" {
  type        = string
  description = "Type of EBS volume"
  default     = "gp3"
}

# Optional network configuration variables
variable "subnet_id" {
  type        = string
  description = "Subnet ID to use for building (optional)"
  default     = ""
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to use for building (optional)"
  default     = ""
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security group IDs to use for building (optional)"
  default     = []
}

variable "iam_instance_profile" {
  type        = string
  description = "IAM instance profile for building (optional)"
  default     = ""
}
