#!/bin/bash
# User data script for AI Inference Server
# This script runs when the instance starts up and configures vLLM service

set -e -x pipefail  # Exit on error, undefined vars, pipe failures

# Set hostname
sudo hostnamectl set-hostname ai-inference

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install NVIDIA GPU drivers
# First, download the NVIDIA GPU drivers from AWS S3
aws s3 cp --recursive s3://ec2-linux-nvidia-drivers/latest/ .
# Then, make the NVIDIA GPU drivers executable
chmod +x NVIDIA-Linux-x86_64*.run
# Finally, install the NVIDIA GPU drivers
sudo ./NVIDIA-Linux-x86_64*.run --no-drm -s

# Create systemd service for vLLM
sudo cat > /etc/systemd/system/vllm.service << 'EOF'
[Unit]
Description=vLLM OpenAI API Server
After=docker.service
Requires=docker.service

[Service]
Type=simple
Restart=always
RestartSec=10
TimeoutStartSec=${vllm_timeout}
User=root
ExecStartPre=/usr/bin/docker pull vllm/vllm-openai:${vllm_version}
ExecStartPre=-/usr/bin/docker stop vllm-server
ExecStartPre=-/usr/bin/docker rm vllm-server
ExecStart=/usr/bin/docker run --runtime nvidia --gpus all \
    -v /root/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=${hugging_face_token}" \
    -p 8000:8000 \
    --ipc=host \
    --name vllm-server \
    vllm/vllm-openai:${vllm_version} \
    --model ${model} ${vllm_args}
ExecStop=/usr/bin/docker stop vllm-server
ExecStopPost=-/usr/bin/docker rm vllm-server

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the vLLM service
sudo systemctl daemon-reload
sudo systemctl enable vllm.service
sudo systemctl start vllm.service

# Clean up
sudo apt-get autoremove -y
sudo apt-get autoclean
