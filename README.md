# AI Engineering

A comprehensive collection of AI engineering projects, infrastructure automation, and learning materials demonstrating practical implementations across cloud infrastructure, AI inference systems, and graph-based AI architectures.

[![OpenTofu](https://img.shields.io/badge/OpenTofu-1.0+-blue.svg)](https://opentofu.org/)
[![Packer](https://img.shields.io/badge/Packer-1.7+-green.svg)](https://packer.io/)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20EBS-orange.svg)](https://aws.amazon.com/)

## 🚀 Quick Start

```bash
# Get available commands and project overview
make help

# Check prerequisites (Packer, AWS CLI, OpenTofu)
make check-prerequisites

# Initialize and setup the project
make setup
```

## 📁 Project Structurex

```text
ai-engineering/
├── Makefile                    # Central automation hub - run `make help`
├── README.md                   # This file
├── infrastructure/             # Cloud infrastructure projects
│   └── ai-inference/           # Production-ready AI inference infrastructure
│       ├── packer/             # Custom Ubuntu 24.04 AMI builder
│       └── opentofu/           # Infrastructure as Code deployment
└── intro-langgraph/            # (Planned) LangGraph learning project
```

## 🎯 Project Goals

This repository serves as a comprehensive portfolio demonstrating:

- **Infrastructure as Code**: Automated cloud infrastructure provisioning
- **AI Inference Systems**: Production-ready AI model deployment
- **DevOps Best Practices**: CI/CD, automation, and monitoring
- **Learning in Public**: Documented journey through AI engineering

## 🏗️ Current Projects

### 1. AI Inference Infrastructure (`infrastructure/ai-inference/`)

A complete infrastructure solution for deploying AI inference workloads on AWS using custom AMIs and OpenTofu.

**Key Features:**

- Custom Ubuntu 24.04 AMI optimized for AI workloads
- GPU-enabled instances (g5.2xlarge with L4 equivalent)
- Automated provisioning with security best practices
- Health monitoring and logging

**Quick Deploy:**

```bash
# Build custom AMI
make ami-build

# Deploy infrastructure
make tofu-plan
make tofu-apply
```

## 🛠️ Technologies

- **Infrastructure**: OpenTofu (Terraform), Packer, AWS (EC2, EBS, VPC)
- **Automation**: Make, Bash scripting, GitHub Actions (planned)
- **AI/ML**: Python, GPU acceleration, model serving frameworks
- **Monitoring**: CloudWatch, custom health checks
- **Security**: EBS encryption, security groups, IAM best practices

## 📋 Available Commands

The project uses a comprehensive Makefile for all operations. Run `make help` to see all available commands:

**Infrastructure Commands:**

- `make ami-build` - Build custom Ubuntu AI inference AMI
- `make tofu-plan` - Plan infrastructure deployment
- `make tofu-apply` - Deploy infrastructure
- `make tofu-destroy` - Tear down infrastructure

**Utility Commands:**

- `make check-prerequisites` - Verify required tools
- `make setup` - Complete project initialization
- `make status` - Show current project status
- `make clean` - Clean build artifacts

## 🚧 Planned Projects

### 2. LangGraph Introduction (`intro-langgraph/`)

- Graph-based AI application development
- Multi-agent systems and workflows
- Integration with various LLM providers

### 3. Additional Infrastructure Components

- Container orchestration (EKS)
- Model serving platforms
- Monitoring and observability stack

## 🔧 Prerequisites

Before using this project, ensure you have:

1. **AWS CLI** configured with appropriate permissions
2. **Packer** 1.7+ for AMI building
3. **OpenTofu** 1.0+ for infrastructure deployment
4. **Make** for automation commands

Quick installation on macOS:

```bash
brew install awscli packer opentofu
```

## 📖 Documentation

Each subproject contains detailed documentation:

- [`infrastructure/ai-inference/packer/README.md`](infrastructure/ai-inference/packer/README.md) - AMI building guide
- [`infrastructure/ai-inference/opentofu/README.md`](infrastructure/ai-inference/opentofu/README.md) - Infrastructure deployment guide

## 🤝 Contributing

This is a personal learning repository, but feedback and suggestions are welcome! Please:

1. Check existing issues and documentation
2. Open an issue for bugs or feature requests  
3. Follow the established code and documentation patterns

## 🎓 Learning Resources

This repository represents practical implementations learned from:

- AWS Well-Architected Framework
- Infrastructure as Code best practices
- AI/ML deployment patterns
- DevOps automation principles

---

*This project demonstrates production-ready infrastructure automation, AI system deployment, and continuous learning in the rapidly evolving field of AI engineering.*
