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


variable "instance_type" {
  description = "EC2 instance type for the AI inference server"
  type        = string
  default     = "g5.2xlarge" # L4 equivalent (8 vCPU, 32 GB RAM, 1 L4 GPU)
}

variable "key_pair_name" {
  description = "Name of the EC2 key pair for SSH access"
  type        = string
}

variable "root_volume_size" {
  description = "Size of the root volume in GB"
  type        = number
  default     = 100
}

variable "additional_volumes" {
  description = "Additional EBS volumes to attach to the instance"
  type = list(object({
    device_name = string
    volume_type = string
    volume_size = number
  }))
  default = [
    {
      device_name = "/dev/sdf"
      volume_type = "gp3"
      volume_size = 500
    }
  ]
}

variable "additional_ports" {
  description = "Additional ports to open in the security group"
  type        = list(number)
  default     = [8000, 8080, 8888] # Common AI inference ports
}

variable "create_eip" {
  description = "Whether to create an Elastic IP for the instance"
  type        = bool
  default     = true
}

variable "disable_api_termination" {
  description = "Whether to disable API termination for the instance"
  type        = bool
  default     = false
}

variable "prevent_destroy" {
  description = "Whether to prevent accidental destruction of the instance"
  type        = bool
  default     = false
}
