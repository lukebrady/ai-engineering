#!/bin/bash
# User data script for AI Inference Server
# This script runs when the instance starts up

set -euo pipefail

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log "Starting AI Inference Server initialization..."

# Update system packages
log "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install additional packages that might be needed
log "Installing additional packages..."
apt-get install -y \
    htop \
    tree \
    jq \
    unzip \
    nginx \
    certbot \
    python3-certbot-nginx

# Create AI inference user
log "Creating AI inference user..."
useradd -m -s /bin/bash -G sudo ai-user
echo 'ai-user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ai-user

# Create AI inference directories
log "Creating AI inference directories..."
mkdir -p /opt/ai-inference/{models,data,logs,scripts}
chown -R ai-user:ai-user /opt/ai-inference

# Set up basic nginx configuration
log "Setting up nginx..."
cat > /etc/nginx/sites-available/ai-inference << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        return 200 "AI Inference Server is running!";
        add_header Content-Type text/plain;
    }
    
    location /health {
        return 200 "healthy";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/ai-inference /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl enable nginx
systemctl start nginx

# Create a simple health check script
log "Creating health check script..."
cat > /opt/ai-inference/health-check.sh << 'EOF'
#!/bin/bash
# Simple health check script

echo "=== AI Inference Server Health Check ==="
echo "Timestamp: $(date)"
echo "Uptime: $(uptime)"
echo "Memory: $(free -h | grep Mem)"
echo "Disk: $(df -h /)"
echo "GPU: $(nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits 2>/dev/null || echo 'No GPU detected')"
echo "================================"
EOF

chmod +x /opt/ai-inference/health-check.sh

# Create systemd service for health monitoring
log "Setting up health monitoring..."
cat > /etc/systemd/system/ai-inference-health.service << 'EOF'
[Unit]
Description=AI Inference Server Health Check
After=network.target

[Service]
Type=oneshot
ExecStart=/opt/ai-inference/health-check.sh
User=ai-user
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create a timer to run health checks
cat > /etc/systemd/system/ai-inference-health.timer << 'EOF'
[Unit]
Description=Run AI Inference Health Check every 5 minutes
Requires=ai-inference-health.service

[Timer]
Unit=ai-inference-health.service
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start the timer
systemctl daemon-reload
systemctl enable ai-inference-health.timer
systemctl start ai-inference-health.timer

# Set up log rotation
log "Setting up log rotation..."
cat > /etc/logrotate.d/ai-inference << 'EOF'
/opt/ai-inference/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 ai-user ai-user
}
EOF

# Create a welcome message
log "Creating welcome message..."
cat > /opt/ai-inference/README.md << 'EOF'
# AI Inference Server

This server has been configured with:
- Ubuntu 24.04 with AI inference tools
- Git and uv for package management
- Nginx web server
- Health monitoring
- Log rotation

## Quick Start

1. SSH into the server: `ssh ai-user@<public-ip>`
2. Check health: `/opt/ai-inference/health-check.sh`
3. View logs: `tail -f /opt/ai-inference/logs/*.log`

## Adding AI Models

1. Navigate to `/opt/ai-inference/models/`
2. Use uv to install Python packages: `uv pip install <package>`
3. Place your models in `/opt/ai-inference/models/`

## Monitoring

- Health checks run every 5 minutes
- Logs are rotated daily
- Nginx serves on port 80
EOF

# Set proper permissions
chown -R ai-user:ai-user /opt/ai-inference
chmod -R 755 /opt/ai-inference

# Final cleanup
log "Performing final cleanup..."
apt-get autoremove -y
apt-get autoclean

log "AI Inference Server initialization completed successfully!"
log "Server is ready for AI inference workloads!"

# Output instance metadata
log "Instance Metadata:"
log "  Environment: ${environment}"
log "  Project: ${project_name}"
log "  Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)"
log "  Instance Type: $(curl -s http://169.254.169.254/latest/meta-data/instance-type)"
log "  Availability Zone: $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)"

hostnamectl set-hostname ai-inference
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install NVIDIA GPU drivers
apt-get install -y gcc make
apt-get upgrade -y linux-aws
apt-get install -y linux-headers-$(uname -r)
cat << EOF | sudo tee --append /etc/modprobe.d/blacklist.conf
blacklist vga16fb
blacklist nouveau
blacklist rivafb
blacklist nvidiafb
blacklist rivatv
EOF
aws s3 cp --recursive s3://ec2-linux-nvidia-drivers/latest/ .
chmod +x NVIDIA-Linux-x86_64*.run
/bin/sh ./NVIDIA-Linux-x86_64*.run

uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto
