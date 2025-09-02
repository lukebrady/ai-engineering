# Key pair variables
variable "key_name" {
  description = "Name of the SSH key pair used for the instance"
  type        = string
  default     = "ai-inference-key"
}

# Instance variables
variable "ami_id" {
  description = "ID of the AMI to use for the instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the AI inference server"
  type        = string
  default     = "g6.xlarge"
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

# IAM variables
variable "iam_instance_profile" {
  description = "IAM instance profile to use for the instance"
  type        = string
}

# VPC variables
variable "vpc_id" {
  description = "ID of the VPC to use for the instance"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet to use for the instance"
  type        = string
}

# Security group variables
variable "additional_ports" {
  description = "Additional ports to open in the security group"
  type        = list(number)
  default     = [8000, 8080, 8888] # Common AI inference ports
}

variable "allowed_ip_addresses" {
  description = "List of IP addresses (CIDR blocks) allowed to access the server"
  type        = list(string)
  default     = [] # Empty list by default - user must specify IPs for security

  validation {
    condition = alltrue([
      for ip in var.allowed_ip_addresses : can(cidrhost(ip, 0))
    ])
    error_message = "All IP addresses must be valid CIDR blocks (e.g., '192.168.1.1/32' or '10.0.0.0/8')."
  }
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

# User data variables
# Can be passed in via TF_VAR_hugging_face_token=<token>
variable "hugging_face_token" {
  description = "Hugging Face token"
  type        = string
  sensitive   = true
}

# Can be passed in via TF_VAR_model=<model>
variable "model" {
  description = "Model to use for inference"
  type        = string
  default     = "Qwen/Qwen3-0.6B"
}

variable "vllm_args" {
  description = "Additional arguments to pass to the vLLM service"
  type        = string
  default     = ""
}

variable "vllm_timeout" {
  description = "Timeout in seconds for the vLLM service to use"
  type        = number
  default     = 360
}

variable "vllm_version" {
  description = "Version of the vLLM service to use"
  type        = string
  default     = "latest"
}
