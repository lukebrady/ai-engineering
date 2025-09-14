# Required Variables
variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the cluster will be deployed"
  type        = string
}

variable "ssh_key_name" {
  description = "Name of the EC2 key pair for SSH access"
  type        = string
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-2"
}

# Optional Variables with Defaults
variable "control_plane_count" {
  description = "Number of control plane instances"
  type        = number
  default     = 1
}

variable "worker_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}

variable "control_plane_instance_type" {
  description = "Instance type for control plane nodes"
  type        = string
  default     = "t3.medium"
}

variable "worker_instance_type" {
  description = "Instance type for worker nodes"
  type        = string
  default     = "t3.large"
}

variable "associate_public_ip" {
  description = "Whether to associate public IP addresses to instances"
  type        = bool
  default     = true
}

# Security Variables
variable "ssh_ingress_cidrs" {
  description = "CIDR blocks allowed to SSH to instances"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "api_ingress_cidrs" {
  description = "CIDR blocks allowed to access Kubernetes API (port 6443)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "nodeport_ingress_cidrs" {
  description = "CIDR blocks allowed to access NodePort services"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# S3 Configuration
variable "create_artifact_bucket" {
  description = "Whether to create an S3 bucket for bootstrap artifacts"
  type        = bool
  default     = true
}

variable "artifact_bucket_name" {
  description = "Name of existing S3 bucket to store join script (if not creating new one)"
  type        = string
  default     = null
}

# Tagging
variable "default_tags" {
  description = "Default tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "ai-inference"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}