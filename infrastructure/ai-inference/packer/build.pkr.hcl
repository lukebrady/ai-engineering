# Build configuration for Ubuntu 24.04 AI Inference AMI

build {
  name = "ubuntu-24.04-ai-inference"

  sources = [
    "source.amazon-ebs.ubuntu"
  ]

  # Provisioner: Execute the main provisioning script
  provisioner "shell" {
    script = "scripts/provision.sh"
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "PYTHONUNBUFFERED=1"
    ]
  }

  # Post-processor: Manifest
  post-processor "manifest" {
    output = "manifest.json"
    strip_path = true
  }
}
