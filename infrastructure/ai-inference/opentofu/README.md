# AI Inference Server - OpenTofu Configuration

This directory contains OpenTofu (formerly Terraform) configuration to deploy an AI inference server using your custom Ubuntu 24.04 AMI.

## Overview

The configuration creates:

- **EC2 Instance**: L4 GPU instance (g5.2xlarge) using your custom AMI
- **Security Group**: Configured for SSH, HTTP, HTTPS, and custom AI inference ports
- **EBS Volumes**: Root volume + additional data volumes
- **Elastic IP**: Static public IP address (optional)
- **Monitoring**: Health checks and logging

## Prerequisites

1. **OpenTofu**: Install OpenTofu 1.0 or later

   ```bash
   # macOS
   brew install opentofu
   
   # Linux
   wget -O- https://apt.releases.opentofu.org/gpg | sudo gpg --dearmor -o /usr/share/keyrings/opentofu-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/opentofu-archive-keyring.gpg] https://apt.releases.opentofu.org $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/opentofu.list
   sudo apt update && sudo apt install opentofu
   ```

   **Note**: The command is `tofu` (not `opentofu`)

2. **AWS CLI**: Configure with appropriate credentials

   ```bash
   aws configure
   ```

3. **Custom AMI**: Build the Ubuntu 24.04 AI Inference AMI first

   ```bash
   cd ../../ai-inference/packer
   make ami-build
   ```

## Configuration

### Required Variables

You must provide these values in `terraform.tfvars`:

- `key_pair_name`: EC2 key pair name for SSH access

Networking uses the default VPC and one of its subnets automatically; no VPC/subnet variables are needed.

### Optional Variables

- `instance_type`: Defaults to `g5.2xlarge` (L4 equivalent)
- `aws_region`: Defaults to `us-east-1`
- `environment`: Defaults to `dev`
- `root_volume_size`: Defaults to 100 GB
- `additional_volumes`: Additional EBS volumes for data/models

## Quick Start

1. **Copy the example configuration**:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit terraform.tfvars** with your values:

   ```bash
   vim terraform.tfvars
   ```

3. **Use the Makefile commands**:

   ```bash
   # Initialize OpenTofu
   make tofu-init
   
   # Plan the deployment
   make tofu-plan
   
   # Deploy the infrastructure
   make tofu-apply
   ```

## Makefile Commands

The project includes a comprehensive Makefile with OpenTofu commands:

### **Core Commands**

- `make tofu-init` - Initialize OpenTofu
- `make tofu-plan` - Show deployment plan
- `make tofu-apply` - Deploy infrastructure
- `make tofu-destroy` - Destroy infrastructure

### **Utility Commands**

- `make tofu-validate` - Validate configuration
- `make tofu-fmt` - Format configuration files
- `make tofu-output` - Show outputs
- `make tofu-refresh` - Refresh state

### **Advanced Commands**

- `make tofu-plan-destroy` - Plan destruction
- `make tofu-import` - Import existing resources
- `make tofu-state` - Manage state
- `make tofu-logs` - Show recent logs

## Instance Types

### **L4 GPU Equivalents**

- `g5.2xlarge`: 8 vCPU, 32 GB RAM, 1 L4 GPU (default)
- `g5.4xlarge`: 16 vCPU, 64 GB RAM, 1 L4 GPU
- `g5.8xlarge`: 32 vCPU, 128 GB RAM, 1 L4 GPU
- `g5.12xlarge`: 48 vCPU, 192 GB RAM, 4 L4 GPUs

### **Other GPU Options**

- `g4dn.xlarge`: 4 vCPU, 16 GB RAM, 1 T4 GPU
- `p3.2xlarge`: 8 vCPU, 61 GB RAM, 1 V100 GPU
- `p4d.24xlarge`: 96 vCPU, 1152 GB RAM, 8 A100 GPUs

## Security Features

- **SSH Access**: Port 22 open (consider restricting in production)
- **Web Access**: Ports 80 (HTTP) and 443 (HTTPS)
- **Custom Ports**: Configurable ports for AI inference services
- **EBS Encryption**: All volumes encrypted at rest
- **Instance Metadata**: IMDSv2 with hop limit protection

## Monitoring & Health Checks

The instance includes:

- **Health Check Script**: `/opt/ai-inference/health-check.sh`
- **Systemd Timer**: Runs health checks every 5 minutes
- **Nginx Health Endpoint**: `http://<ip>/health`
- **Log Rotation**: Daily log rotation with compression
- **CloudWatch Integration**: Basic monitoring enabled

## User Management

- **Default User**: `ai-user` with sudo access
- **SSH Access**: Use your configured key pair
- **Home Directory**: `/home/ai-user`
- **AI Directory**: `/opt/ai-inference/`

## Cost Optimization

- **Spot Instances**: Consider using spot instances for development
- **EBS Optimization**: Use gp3 volumes for better performance/cost ratio
- **Auto Scaling**: Implement auto-scaling for production workloads
- **Reserved Instances**: Use RIs for predictable workloads

## Troubleshooting

### **Common Issues**

1. **AMI Not Found**: Ensure you've built the AMI first
2. **VPC/Subnet**: Uses the default VPC and one of its subnets automatically
3. **Key Pair Issues**: Ensure the key pair exists in the region
4. **Permission Errors**: Check IAM roles and policies

### **Debug Commands**

```bash
# Check instance status
make tofu-output

# View instance logs
aws ec2 get-console-output --instance-id <instance-id>

# SSH into instance
ssh -i <key-file> ai-user@<public-ip>

# Check health
curl http://<public-ip>/health
```

## Next Steps

Once deployed:

1. **SSH into the instance**: `ssh ai-user@<public-ip>`
2. **Install AI packages**: Use `uv pip install <package>`
3. **Deploy models**: Place models in `/opt/ai-inference/models/`
4. **Configure services**: Set up your AI inference endpoints
5. **Monitor performance**: Use the health check scripts

## Support

For issues:

1. Check OpenTofu documentation
2. Verify AWS credentials and permissions
3. Ensure all required variables are set
4. Check the instance console output for errors
