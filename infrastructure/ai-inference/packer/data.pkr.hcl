# Data sources for Ubuntu 24.04 AI Inference AMI

data "amazon-ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filters = {
    name   = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    virtualization-type = "hvm"
    root-device-type = "ebs"
    architecture = "x86_64"
  }
}

data "amazon-parameterstore" "ai_inference_profile" {
  name = "ai-inference-profile"
  with_decryption = false
}
