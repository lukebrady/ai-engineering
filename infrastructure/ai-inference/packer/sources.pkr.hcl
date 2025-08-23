# Build sources for Ubuntu 24.04 AI Inference AMI

locals {
  # ISO-8601 timestamp formats
  ami_timestamp = "{{isotime \"2006-01-02T15-04-05\"}}"  # AMI-compatible (no colons)
  tag_timestamp = "{{isotime \"2006-01-02T15:04:05\"}}"  # Proper ISO-8601 with colons
}

source "amazon-ebs" "ubuntu" {
  ami_name        = "${var.ami_name_prefix}-${local.ami_timestamp}"
  ami_description = var.ami_description
  instance_type   = var.instance_type
  region          = var.aws_region
  source_ami      = data.amazon-ami.ubuntu.id

  # SSH configuration
  ssh_username = var.ssh_username
  ssh_timeout  = "10m"

  # EBS configuration - using launch_block_device_mappings for volume configuration
  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = var.volume_size
    volume_type = var.volume_type
    delete_on_termination = true
  }
  
  # Tags
  run_tags = {
    Name          = "${var.ami_name_prefix}-${local.ami_timestamp}"
    Environment   = "development"
    Purpose       = "ai-inference"
    OS            = "ubuntu-24.04"
    BuildDate     = local.tag_timestamp
    PackerVersion = "{{packer_version}}"
  }
}