# Data source for the latest Ubuntu 24.04 AI Inference AMI
data "aws_ami" "ai_inference" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["${var.ami_name_prefix}*"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# Security group for the AI inference server
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_iam_instance_profile" "ai_inference_profile" {
  name = "ai-inference-profile"
}
