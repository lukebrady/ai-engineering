# AI Inference Infrastructure - OpenTofu

This directory contains modular OpenTofu (Terraform) configurations for deploying AI inference infrastructure on AWS. The infrastructure is organized into separate components for better maintainability and reusability.

## 📁 Directory Structure

```text
opentofu/
├── README.md                   # This file
├── iam/                        # IAM roles and policies
│   ├── main.tf                 # IAM role definitions
│   ├── outputs.tf              # IAM outputs (role ARNs, instance profile)
│   ├── providers.tf            # AWS provider configuration
│   └── variables.tf            # IAM variables
├── inference/                  # Main inference deployment
│   ├── data.tf                 # Data sources (AMI, VPC, subnets)
│   ├── main.tf                 # Module instantiation for multiple models
│   ├── outputs.tf              # Inference outputs (IPs, DNS names)
│   ├── providers.tf            # AWS provider configuration
│   ├── secure.tfvars           # Secure variables (HuggingFace token)
│   └── variables.tf            # Inference variables
└── modules/
    └── inference/              # Reusable inference server module
        ├── main.tf             # EC2 instance, security groups, SSH keys
        ├── outputs.tf          # Module outputs
        ├── providers.tf        # Provider requirements
        ├── scripts/
        │   └── user_data.sh    # Instance initialization script
        └── variables.tf        # Module variables
```

## 🏗️ Architecture Overview

The infrastructure follows a modular approach:

1. **IAM Module** (`iam/`) - Creates necessary IAM roles and instance profiles
2. **Inference Module** (`inference/`) - Deploys multiple AI inference servers using the reusable module
3. **Reusable Module** (`modules/inference/`) - Parameterized module for creating inference servers

### Current Deployment

The `inference/main.tf` currently deploys three model configurations:

- **Qwen 3 0.6B** - Lightweight model for testing (`Qwen/Qwen3-0.6B`) on g5.2xlarge
- **GPT-OSS 20B** - Medium-sized model for production workloads (`openai/gpt-oss-20b`) on g5.2xlarge
- **Gemma 3 27B** - Large model for high-performance inference (`google/gemma-3-27b-it`) on g6.12xlarge with 4-GPU tensor parallelism

## 🚀 Quick Start

### Prerequisites

1. **AWS CLI** configured with appropriate permissions
2. **OpenTofu** 1.0+ installed
3. **HuggingFace token** for model access

### Deployment Steps

1. **Deploy IAM resources first:**
   ```bash
   make tofu-iam-apply
   ```

2. **Configure secure variables:**
   ```bash
   # Edit secure.tfvars with your HuggingFace token
   cd infrastructure/ai-inference/opentofu/inference
   cp secure.tfvars.example secure.tfvars
   # Edit the file with your actual token
   ```

3. **Deploy inference infrastructure:**
   ```bash
   make tofu-inference-apply
   ```

4. **Get output information:**
   ```bash
   make tofu-output
   ```

## 🛠️ Available Make Commands

### Complete Workflow
```bash
make tofu-apply          # Deploy all infrastructure (IAM + inference)
make tofu-destroy        # Destroy all infrastructure
```

### Individual Components
```bash
# IAM Module
make tofu-iam-init       # Initialize IAM module
make tofu-iam-plan       # Show IAM deployment plan
make tofu-iam-apply      # Deploy IAM resources
make tofu-iam-destroy    # Destroy IAM resources

# Inference Module
make tofu-inference-init     # Initialize inference module
make tofu-inference-plan     # Show inference deployment plan
make tofu-inference-apply    # Deploy inference infrastructure
make tofu-inference-destroy  # Destroy inference infrastructure

# Modules (for development)
make tofu-modules-init       # Initialize reusable modules
make tofu-modules-validate   # Validate module code
make tofu-modules-fmt        # Format module code
```

### Validation & Formatting
```bash
make tofu-validate       # Validate all configurations
make tofu-fmt           # Format all Terraform files
make tofu-init          # Initialize all modules
```

### Utilities
```bash
make tofu-output        # Show all outputs
make tofu-state         # Show current state
make tofu-refresh       # Refresh state from AWS
```

## 📋 Configuration

### IAM Module Variables

The IAM module creates the following resources:
- EC2 instance role with necessary permissions
- Instance profile for EC2 instances
- Policies for accessing ECR, S3, and CloudWatch

### Inference Module Variables

Key variables for the inference deployment:

| Variable | Description | Default |
|----------|-------------|---------|
| `hugging_face_token` | HuggingFace API token (required) | - |
| `allowed_ip_addresses` | CIDR blocks for SSH/HTTPS access | `[]` |

### Module Variables

The reusable inference module accepts:

| Variable | Description | Default |
|----------|-------------|---------|
| `model` | HuggingFace model identifier | - |
| `instance_type` | EC2 instance type | `g5.2xlarge` |
| `vllm_version` | vLLM Docker image version | `latest` |
| `vllm_timeout` | Model loading timeout in seconds | `300` |
| `vllm_args` | Additional vLLM arguments | `""` |
| `key_name` | SSH key pair name | - |
| `additional_ports` | Additional ports for security group | `[8000]` |

## 🔒 Security Features

- **EBS Encryption**: All volumes encrypted at rest
- **Security Groups**: Restrictive inbound rules based on allowed IP addresses
- **IAM Roles**: Least privilege principle with specific permissions
- **SSH Keys**: Automatically generated and managed per deployment
- **Instance Metadata**: IMDSv2 enforced for enhanced security

## 🌐 Outputs

After deployment, the following outputs are available:

### IAM Outputs
- `ai_inference_role_arn` - ARN of the IAM role
- `ai_inference_instance_profile_name` - Instance profile name

### Inference Outputs
- `qwen3_0_6b_public_ip` - Public IP of Qwen model instance
- `qwen3_0_6b_private_ip` - Private IP of Qwen model instance
- `gpt_oss_20b_public_ip` - Public IP of GPT-OSS model instance
- `gpt_oss_20b_private_ip` - Private IP of GPT-OSS model instance
- `gemma_3_27b_public_ip` - Public IP of Gemma model instance
- `gemma_3_27b_private_ip` - Private IP of Gemma model instance
- SSH connection commands for each instance

## 🔧 Customization

### Adding New Models

To deploy additional models, add new module blocks in `inference/main.tf`:

```hcl
module "new_model" {
  source = "../modules/inference"

  ami_id               = data.aws_ami.ai_inference.id
  vpc_id               = data.aws_vpc.default.id
  subnet_id            = data.aws_subnets.default.ids[0]
  iam_instance_profile = data.aws_iam_instance_profile.ai_inference_profile.name
  key_name             = "new_model_key"
  
  allowed_ip_addresses = var.allowed_ip_addresses
  hugging_face_token   = var.hugging_face_token
  model                = "organization/model-name"
  instance_type        = "g5.2xlarge"  # Choose appropriate instance
  vllm_timeout         = 300
  vllm_version         = "latest"
}
```

### Instance Type Selection

Choose appropriate instance types based on model size:

- **Small models (< 1B parameters)**: `g5.xlarge` or `g5.2xlarge`
- **Medium models (1B-10B parameters)**: `g5.4xlarge` or `g5.8xlarge`
- **Large models (10B+ parameters)**: `g6.12xlarge`, `g6.16xlarge`, or `p4d.24xlarge`

For multi-GPU deployments, use `vllm_args = "--tensor-parallel-size=N"` where N is the number of GPUs.

### Tensor Parallelism Configuration

For large models requiring multiple GPUs:

```hcl
module "large_model" {
  # ... other configuration
  instance_type = "g6.12xlarge"          # 4 GPUs
  vllm_args     = "--tensor-parallel-size=4"  # Distribute across 4 GPUs
  vllm_timeout  = 900                     # Longer timeout for large models
}
```

## 💰 Cost Considerations

GPU instances can be expensive. Current approximate hourly costs (us-east-1):

- **g5.2xlarge**: ~$1.21/hour (1 GPU, 8 vCPUs, 32 GB RAM)
- **g6.12xlarge**: ~$5.17/hour (4 GPUs, 48 vCPUs, 192 GB RAM)
- **p4d.24xlarge**: ~$32.77/hour (8 GPUs, 96 vCPUs, 1152 GB RAM)

**Cost Management Tips:**
- Use Spot Instances for development/testing (add `instance_market_options` in module)
- Set up CloudWatch alarms for cost monitoring
- Consider scheduled start/stop for non-production workloads
- Use smaller instance types for model evaluation before scaling up

## 🚨 Important Notes

1. **HuggingFace Token**: Required for accessing gated models. Store in `secure.tfvars` and never commit to version control.

2. **Security**: The deployment creates security groups that only allow access from specified IP addresses. Update `allowed_ip_addresses` for proper access control.

3. **Dependencies**: The inference module depends on the IAM module. Deploy IAM resources first.

4. **SSH Access**: Private keys are generated automatically and stored in the modules directory. Keep these secure and don't commit to version control.

5. **Model Loading Time**: Large models (especially Gemma 27B) can take 10-15 minutes to load. Monitor CloudWatch logs or SSH into instances to check progress.

## 🧹 Cleanup

To completely remove all infrastructure:

```bash
make tofu-destroy  # Destroys inference first, then IAM
```

Or destroy components individually:

```bash
make tofu-inference-destroy  # Remove inference infrastructure
make tofu-iam-destroy       # Remove IAM resources
```

---

*This infrastructure provides a production-ready foundation for deploying AI inference workloads on AWS with proper security, monitoring, and scalability considerations.*