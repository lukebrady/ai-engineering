# Data sources for existing infrastructure
data "aws_subnets" "control_plane" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }

  # Filter subnets by tag key/value
  filter {
    name   = "tag:SubnetType"
    values = ["NAT-Instance"]
  }
}

data "aws_subnets" "worker" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }

  # Filter subnets by tag key/value
  filter {
    name   = "tag:SubnetType"
    values = ["NAT-Instance"]
  }
}
