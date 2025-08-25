#!/bin/bash
# User data script for AI Inference Server
# This script runs when the instance starts up and configures vLLM service

set -e -x pipefail  # Exit on error, undefined vars, pipe failures

# Update system
sudo apt-get update
sudo apt-get upgrade -y

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
User=root
Environment="HUGGING_FACE_HUB_TOKEN=${hugging_face_token}"
Environment="MODEL=${model}"
ExecStartPre=/usr/bin/docker pull vllm/vllm-openai:latest
ExecStartPre=-/usr/bin/docker stop vllm-server
ExecStartPre=-/usr/bin/docker rm vllm-server
ExecStart=/usr/bin/docker run --runtime nvidia --gpus all \
    -v /root/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN}" \
    -p 8000:8000 \
    --ipc=host \
    --name vllm-server \
    vllm/vllm-openai:latest \
    --model $MODEL
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
