# Ubuntu 24.04 AI Inference AMI Builder

This directory contains Packer configurations to build a custom Ubuntu 24.04 AMI optimized for AI inference workloads.

## Prerequisites

1. **Packer**: Install Packer 1.7.0 or later
   ```bash
   # macOS
   brew install packer
   
   # Linux
   wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install packer
   ```

2. **AWS CLI**: Configure with appropriate credentials
   ```bash
   aws configure
   ```

3. **IAM Permissions**: Ensure your AWS user/role has the following permissions:
   - `ec2:RunInstances`
   - `ec2:StopInstances`
   - `ec2:TerminateInstances`
   - `ec2:CreateImage`
   - `ec2:DeregisterImage`
   - `ec2:DescribeImages`
   - `ec2:DescribeInstances`
   - `ec2:CreateTags`
   - `ec2:CreateSnapshot`
   - `ec2:DeleteSnapshot`
   - `ec2:DescribeSnapshots`

## Configuration

### Design Philosophy

This project follows a **"start simple, iterate fast"** approach:

1. **Baseline First**: Get a minimal working foundation
2. **Minimal Dependencies**: Only essential tools (git, uv)
3. **Easy to Extend**: Simple structure for adding features
4. **Fast Builds**: Quick iteration cycles

### File Organization

The Packer configuration is organized into separate files following HCL2 best practices:

- **`packer.pkr.hcl`** - Main entry point (automatically reads all other files)
- **`plugins.pkr.hcl`** - Plugin requirements and versions
- **`variables.pkr.hcl`** - Variable declarations with types and descriptions
- **`data.pkr.hcl`** - Data sources for AMI selection
- **`sources.pkr.hcl`** - Build source configurations
- **`build.pkr.hcl`** - Build configuration (uses external script)
- **`scripts/provision.sh`** - Main provisioning script with all system configuration
- **`local.pkr.hcl`** - Local customizations (gitignored)

### Variables

Edit `variables.pkr.hcl` to customize:
- AWS region
- Instance type for building
- AMI naming conventions
- Network configuration (optional)

For local customizations, edit `local.pkr.hcl` (this file is gitignored).

### Security Groups

The configuration uses the default security group. Ensure it allows SSH access (port 22) from your IP.

## Usage

### Build the AMI

```bash
# Initialize Packer (first time only)
packer init .

# Validate the configuration
packer validate .

# Build the AMI
packer build .

# Build with custom variables
packer build -var="aws_region=us-west-2" -var="instance_type=t3.large" .
```

### Build with Variables File

```bash
# Use local customizations
packer build -var-file="local.pkr.hcl" .

# Or override specific variables
packer build -var="aws_region=us-west-2" -var="instance_type=t3.large" .
```

### Build Specific Components

```bash
# Build only the Ubuntu AMI
packer build -only=amazon-ebs.ubuntu .
```

## Output

After successful build, you'll get:
- AMI ID in the specified region
- `manifest.json` file with build details
- EBS snapshot for the AMI

## Customization

### Adding AI Inference Tools

To add specific AI inference tools, modify the `scripts/provision.sh` file:

```bash
# Example: Install Python packages with uv
install_python_packages() {
    log "Installing Python packages..."
    
    # Use uv to install packages
    uv pip install numpy pandas scipy scikit-learn
    
    log "Python packages installed successfully"
}

# Example: Install CUDA
install_cuda() {
    log "Installing CUDA toolkit..."
    
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    sudo apt-get install -y cuda-toolkit
    
    log "CUDA toolkit installed successfully"
}

# Then add the function calls to the main() function
```

### Common AI Tools to Consider

- **CUDA Toolkit**: For GPU acceleration
- **PyTorch/TensorFlow**: Deep learning frameworks
- **ONNX Runtime**: Model inference optimization
- **Docker**: Containerization
- **NVIDIA drivers**: GPU support
- **Python packages**: numpy, pandas, scikit-learn

## Troubleshooting

### Common Issues

1. **SSH Timeout**: Increase `ssh_timeout` in the configuration
2. **Permission Denied**: Check IAM permissions
3. **Security Group Issues**: Ensure SSH access is allowed
4. **Build Failure**: Check the Packer logs for specific error messages

### Debug Mode

```bash
packer build -debug .
```

### Logs

Packer logs are displayed in real-time. For persistent logging:
```bash
packer build . 2>&1 | tee build.log
```

## Security Considerations

- The AMI includes basic security hardening
- Consider adding additional security measures:
  - Firewall configuration
  - Security updates automation
  - User access controls
  - Audit logging

## Cost Optimization

- Use spot instances for building (if available)
- Choose appropriate instance types
- Clean up unused AMIs and snapshots
- Monitor EBS usage

## Next Steps

Once you have the base AMI, you can:
1. Add specific AI inference tools
2. Configure model serving frameworks
3. Set up monitoring and logging
4. Create deployment automation
5. Test with your specific workloads

## Support

For issues with this Packer configuration:
1. Check Packer documentation
2. Review AWS AMI building best practices
3. Validate your AWS credentials and permissions
4. Ensure all required plugins are installed
