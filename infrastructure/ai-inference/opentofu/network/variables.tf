variable "availability_zones" {
  description = "Availability zones to create subnets in"
  type        = set(string)
  default = [
    "us-east-1a",
    "us-east-1b",
  ]
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
