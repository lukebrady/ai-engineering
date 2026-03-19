# AI Engineering

A comprehensive collection of AI engineering projects designed as an **executable codebase** - where both humans and AI agents can discover and run available tools through a unified interface. This repository demonstrates practical implementations across cloud infrastructure, AI inference systems, and graph-based AI architectures.

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

## 📁 Project Structure

```text
ai-engineering/
├── Makefile                    # 🎯 EXECUTABLE INTERFACE - Universal tool catalog
├── README.md                   # This file
├── .github/workflows/          # CI/CD automation for tool validation
├── agents/                     # AI agent implementations and examples
│   └── oss-agent/             # Example agent using open source models
├── infrastructure/             # Cloud infrastructure projects
│   └── ai-inference/           # Production-ready AI inference infrastructure
│       ├── packer/             # Custom Ubuntu 24.04 AMI builder with GPU support
│       └── opentofu/           # Modular Infrastructure as Code deployment
│           ├── iam/            # IAM roles and permissions
│           ├── inference/      # Main deployment using modular components
│           └── modules/        # Reusable Terraform modules
│               └── inference/  # Parameterized inference server module
└── intro-langgraph/            # (Planned) LangGraph learning project
```

## 🎯 Project Philosophy: Executable Codebase

This repository embodies a core principle: **the codebase itself should be executable by both humans and AI agents**. Every tool, command, and capability is discoverable and runnable through a unified interface.

### For AI Agents 🤖

```bash
make help  # Same interface - AI agents can parse and execute tools
```

**Key Principles:**

- **Single Source of Truth**: The Makefile serves as the authoritative catalog of all executable operations
- **Self-Documenting**: Every command includes clear descriptions and usage examples
- **Universal Access**: The same interface works for humans, CI/CD systems, and AI agents
- **Discoverability**: No hidden commands - everything is accessible via `make help`

## 🎯 Project Goals

This repository serves as a comprehensive portfolio demonstrating:

- **Infrastructure as Code**: Automated cloud infrastructure provisioning
- **AI Inference Systems**: Production-ready AI model deployment  
- **DevOps Best Practices**: CI/CD, automation, and monitoring
- **Human-AI Collaboration**: Interfaces designed for both human and AI agent interaction
- **Learning in Public**: Documented journey through AI engineering

## 🏗️ Current Projects

### 1. AI Inference Infrastructure (`infrastructure/ai-inference/`)

A complete infrastructure solution for deploying AI inference workloads on AWS using custom AMIs and modular OpenTofu configuration.

**Key Features:**

- Custom Ubuntu 24.04 AMI with Docker, NVIDIA drivers, and GPU support
- Modular architecture: separate IAM, inference, and reusable modules
- Multi-model deployment: Qwen 3 0.6B, GPT-OSS 20B, and Gemma 3 27B configurations
- vLLM server with systemd integration and container lifecycle management
- GPU-enabled instances (g5.2xlarge) with automated provisioning
- Comprehensive security: EBS encryption, restrictive security groups, IAM best practices

**Quick Deploy:**

```bash
# Build custom AMI
make ami-build

# Deploy IAM resources
make tofu-iam-apply

# Deploy inference infrastructure
make tofu-inference-apply
```

### 2. OSS Agent Example (`agents/oss-agent/`)

A practical example of building AI agents using open source models with comprehensive documentation.

**Key Features:**

- OpenAI-compatible API integration for local models (vLLM, Ollama)
- Function calling with Wikipedia search tools
- Interactive REPL with Rich formatting
- Comprehensive comments explaining agent patterns and OSS model usage

**Quick Start:**

```bash
cd agents/oss-agent
python main.py  # Interactive agent with Wikipedia search
```

## 🛠️ Technologies

- **Infrastructure**: OpenTofu (Terraform), Packer, AWS (EC2, EBS, VPC, IAM)
- **AI/ML**: vLLM, Python, GPU acceleration, OpenAI-compatible APIs
- **Containerization**: Docker, systemd service management
- **Automation**: Make, Bash scripting, GitHub Actions
- **Security**: EBS encryption, security groups, IAM best practices

## 📋 Executable Tool Catalog

The project's **Makefile serves as the executable interface** - a programmatically parseable catalog of all available tools. This design enables both humans and AI agents to discover and execute operations using the same commands.

### 🔍 Tool Discovery

```bash
make help  # Lists all available tools with descriptions
```

**Example Output:**

```text
AI Engineering - Executable Tool Catalog

AMI/Packer Commands:
  ami-build                 Build the AMI (with validation)
  ami-init                  Initialize Packer plugins
  ami-validate              Validate Packer configuration

Agent Commands:
  agent-oss-check           Check OSS agent environment and dependencies
  agent-oss-install         Install OSS agent dependencies
  agent-oss-run             Run the OSS agent interactively

Infrastructure/OpenTofu Commands:
  tofu-apply                Deploy all infrastructure with OpenTofu
  tofu-iam-apply            Deploy IAM infrastructure with OpenTofu
  tofu-inference-apply      Deploy inference infrastructure with OpenTofu
  tofu-init                 Initialize all OpenTofu modules
  tofu-plan                 Show deployment plan for all modules
  tofu-validate             Validate all OpenTofu modules

Setup & Verification Commands:
  check-aws-config          Check AWS configuration and permissions
  check-prerequisites       Check if required tools are installed
  setup                     Complete setup and initialization

Utility Commands:
  help                      Show this help message
  list-ami                  List recent AMIs created by this project
  status                    Show current project status
```

### 🤖 AI Agent Compatibility

The Makefile format is specifically designed to be:

- **Parseable**: AI agents can extract command names and descriptions
- **Executable**: Commands can be run programmatically
- **Self-Contained**: Each command includes all necessary context
- **Consistent**: Uniform pattern across all operations

### 📊 Tool Categories

**Infrastructure Commands:**

- `make ami-build` - Build custom Ubuntu AI inference AMI
- `make tofu-iam-apply` - Deploy IAM resources (roles, policies)
- `make tofu-inference-apply` - Deploy inference infrastructure (EC2, vLLM)
- `make tofu-apply` - Deploy all infrastructure (IAM + inference)
- `make tofu-destroy` - Tear down all infrastructure

**Agent Commands:**

- `make agent-oss-run` - Run the OSS agent interactively
- `make agent-oss-install` - Install OSS agent dependencies
- `make agent-oss-check` - Check agent environment and dependencies

**Utility Commands:**

- `make check-prerequisites` - Verify required tools
- `make setup` - Complete project initialization
- `make status` - Show current project status
- `make clean` - Clean build artifacts

**Validation Commands:**

- `make ami-validate` - Validate Packer configuration
- `make tofu-validate` - Validate OpenTofu configuration

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
- [`infrastructure/ai-inference/opentofu/README.md`](infrastructure/ai-inference/opentofu/README.md) - Complete infrastructure deployment guide
- [`agents/oss-agent/main.py`](agents/oss-agent/main.py) - Comprehensive agent implementation with inline documentation

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
