variable "ami_name_prefix" {
  description = "Prefix for the AMI name"
  type        = string
  default     = "ai-inference-ubuntu-24-04"
}

variable "allowed_ip_addresses" {
  description = "List of IP addresses (CIDR blocks) allowed to access the server"
  type        = list(string)
}

variable "hugging_face_token" {
  description = "Hugging Face token"
  type        = string
  sensitive   = true
}
