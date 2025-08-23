# Makefile for AI Engineering Project
# Provides easy commands for building and managing Packer AMIs

# Configuration
PACKER_DIR := infrastructure/ai-inference/packer
PACKER_CONFIG := $(PACKER_DIR)
PACKER_LOG_FILE := $(PACKER_DIR)/packer-build.log

# Default values
AWS_REGION ?= us-east-1
INSTANCE_TYPE ?= t3.medium
AMI_NAME_PREFIX ?= ubuntu-24.04-ai-inference

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Help target (default)
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)AI Engineering Project - Packer AMI Builder$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Environment variables:$(NC)"
	@echo "  AWS_REGION         AWS region for building (default: us-east-1)"
	@echo "  INSTANCE_TYPE      EC2 instance type for building (default: t3.medium)"
	@echo "  AMI_NAME_PREFIX    Prefix for AMI names (default: ubuntu-24.04-ai-inference)"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make ami-build                           # Build AMI with defaults"
	@echo "  make ami-build AWS_REGION=us-west-2     # Build in specific region"
	@echo "  make ami-build INSTANCE_TYPE=t3.large   # Use larger instance type"

# Packer commands
.PHONY: ami-init
ami-init: ## Initialize Packer plugins
	@echo "$(BLUE)Initializing Packer plugins...$(NC)"
	@cd $(PACKER_CONFIG) && packer init .

.PHONY: ami-validate
ami-validate: ## Validate Packer configuration
	@echo "$(BLUE)Validating Packer configuration...$(NC)"
	@cd $(PACKER_CONFIG) && packer validate .

.PHONY: ami-build
ami-build: ami-init ami-validate ## Build the AMI (with validation)
	@echo "$(BLUE)Building AMI with region: $(AWS_REGION), instance: $(INSTANCE_TYPE)$(NC)"
	@cd $(PACKER_CONFIG) && packer build \
		-var="aws_region=$(AWS_REGION)" \
		-var="instance_type=$(INSTANCE_TYPE)" \
		-var="ami_name_prefix=$(AMI_NAME_PREFIX)" \
		. 2>&1 | tee $(PACKER_LOG_FILE)
	@echo "$(GREEN)AMI build completed! Check $(PACKER_LOG_FILE) for details.$(NC)"

.PHONY: ami-build-debug
ami-build-debug: ami-init ami-validate ## Build the AMI in debug mode
	@echo "$(BLUE)Building AMI in debug mode...$(NC)"
	@cd $(PACKER_CONFIG) && packer build -debug \
		-var="aws_region=$(AWS_REGION)" \
		-var="instance_type=$(INSTANCE_TYPE)" \
		-var="ami_name_prefix=$(AMI_NAME_PREFIX)" \
		. 2>&1 | tee $(PACKER_LOG_FILE)

.PHONY: ami-build-local
ami-build-local: ami-init ami-validate ## Build AMI using local.pkr.hcl variables
	@echo "$(BLUE)Building AMI using local variables...$(NC)"
	@cd $(PACKER_CONFIG) && packer build \
		-var-file="local.pkr.hcl" \
		. 2>&1 | tee $(PACKER_LOG_FILE)

.PHONY: test-provision-script
test-provision-script: ## Test the provision script locally (requires Ubuntu environment)
	@echo "$(BLUE)Testing provision script...$(NC)"
	@if [ -f $(PACKER_CONFIG)/scripts/provision.sh ]; then \
		echo "$(GREEN)Provision script found and is executable$(NC)"; \
		echo "$(BLUE)Script size: $(shell wc -l < $(PACKER_CONFIG)/scripts/provision.sh) lines$(NC)"; \
		echo "$(BLUE)To test locally, run: cd $(PACKER_CONFIG)/scripts && ./provision.sh$(NC)"; \
	else \
		echo "$(RED)Provision script not found!$(NC)"; \
	fi

# OpenTofu commands
.PHONY: tofu-init
tofu-init: ## Initialize OpenTofu configuration
	@echo "$(BLUE)Initializing OpenTofu configuration...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu init

.PHONY: tofu-validate
tofu-validate: ## Validate OpenTofu configuration
	@echo "$(BLUE)Validating OpenTofu configuration...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu validate

.PHONY: tofu-fmt
tofu-fmt: ## Format OpenTofu configuration files
	@echo "$(BLUE)Formatting OpenTofu configuration files...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu fmt

.PHONY: tofu-plan
tofu-plan: tofu-init tofu-validate ## Show OpenTofu deployment plan
	@echo "$(BLUE)Showing OpenTofu deployment plan...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu plan -var-file=secure.tfvars

.PHONY: tofu-apply
tofu-apply: tofu-init tofu-validate ## Deploy infrastructure with OpenTofu
	@echo "$(BLUE)Deploying infrastructure with OpenTofu...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu apply -var-file=secure.tfvars -auto-approve

.PHONY: tofu-destroy
tofu-destroy: ## Destroy infrastructure with OpenTofu
	@echo "$(BLUE)Destroying infrastructure with OpenTofu...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu destroy -auto-approve

.PHONY: tofu-plan-destroy
tofu-plan-destroy: ## Show OpenTofu destruction plan
	@echo "$(BLUE)Showing OpenTofu destruction plan...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu plan -destroy

.PHONY: tofu-output
tofu-output: ## Show OpenTofu outputs
	@echo "$(BLUE)Showing OpenTofu outputs...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu output

.PHONY: tofu-refresh
tofu-refresh: ## Refresh OpenTofu state
	@echo "$(BLUE)Refreshing OpenTofu state...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu refresh

.PHONY: tofu-state
tofu-state: ## Show OpenTofu state
	@echo "$(BLUE)Showing OpenTofu state...$(NC)"
	@cd infrastructure/ai-inference/opentofu && tofu show

.PHONY: tofu-logs
tofu-logs: ## Show recent OpenTofu logs
	@echo "$(BLUE)Recent OpenTofu logs:$(NC)"
	@if [ -f infrastructure/ai-inference/opentofu/.terraform/logs/tofu.log ]; then \
		tail -50 infrastructure/ai-inference/opentofu/.terraform/logs/tofu.log; \
	else \
		echo "$(YELLOW)No OpenTofu logs found. Run 'make tofu-init' first.$(NC)"; \
	fi

.PHONY: ami-clean
ami-clean: ## Clean up build artifacts and logs
	@echo "$(BLUE)Cleaning up build artifacts...$(NC)"
	@rm -f $(PACKER_LOG_FILE)
	@rm -f $(PACKER_CONFIG)/manifest.json
	@echo "$(GREEN)Cleanup completed!$(NC)"

.PHONY: ami-logs
ami-logs: ## Show the latest build logs
	@if [ -f $(PACKER_LOG_FILE) ]; then \
		echo "$(BLUE)Latest build logs:$(NC)"; \
		tail -50 $(PACKER_LOG_FILE); \
	else \
		echo "$(YELLOW)No build logs found. Run 'make ami-build' first.$(NC)"; \
	fi

.PHONY: ami-logs-follow
ami-logs-follow: ## Follow build logs in real-time
	@if [ -f $(PACKER_LOG_FILE) ]; then \
		echo "$(BLUE)Following build logs (Ctrl+C to stop):$(NC)"; \
		tail -f $(PACKER_LOG_FILE); \
	else \
		echo "$(YELLOW)No build logs found. Run 'make ami-build' first.$(NC)"; \
	fi

# Development and testing
.PHONY: check-prerequisites
check-prerequisites: ## Check if required tools are installed
	@echo "$(BLUE)Checking prerequisites...$(NC)"
	@command -v packer >/dev/null 2>&1 || { echo "$(RED)Error: Packer is not installed$(NC)"; exit 1; }
	@command -v aws >/dev/null 2>&1 || { echo "$(RED)Error: AWS CLI is not installed$(NC)"; exit 1; }
	@command -v tofu >/dev/null 2>&1 || { echo "$(YELLOW)Warning: OpenTofu is not installed$(NC)"; echo "$(BLUE)Install with: brew install opentofu$(NC)"; }
	@packer version | head -1
	@aws --version
	@command -v tofu >/dev/null 2>&1 && tofu version | head -1 || echo "$(YELLOW)OpenTofu not available$(NC)"
	@echo "$(GREEN)Core prerequisites are satisfied!$(NC)"

.PHONY: check-aws-config
check-aws-config: ## Check AWS configuration and permissions
	@echo "$(BLUE)Checking AWS configuration...$(NC)"
	@aws sts get-caller-identity >/dev/null 2>&1 || { echo "$(RED)Error: AWS credentials not configured or invalid$(NC)"; exit 1; }
	@echo "$(GREEN)AWS credentials are valid!$(NC)"
	@echo "$(BLUE)Current AWS account: $(shell aws sts get-caller-identity --query 'Account' --output text)$(NC)"
	@echo "$(BLUE)Current AWS region: $(shell aws configure get region)$(NC)"

.PHONY: install-opentofu
install-opentofu: ## Install OpenTofu (macOS)
	@echo "$(BLUE)Installing OpenTofu...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew install opentofu; \
		echo "$(GREEN)OpenTofu installed successfully!$(NC)"; \
	else \
		echo "$(RED)Error: Homebrew not found. Please install OpenTofu manually.$(NC)"; \
		echo "$(BLUE)Visit: https://opentofu.org/docs/intro/install/$(NC)"; \
		exit 1; \
	fi

.PHONY: setup
setup: check-prerequisites check-aws-config ami-init ## Complete setup and initialization
	@echo "$(GREEN)Setup completed successfully!$(NC)"

# Utility targets
.PHONY: status
status: ## Show current project status
	@echo "$(BLUE)Project Status:$(NC)"
	@echo "  Packer config directory: $(PACKER_CONFIG)"
	@echo "  AWS region: $(AWS_REGION)"
	@echo "  Instance type: $(INSTANCE_TYPE)"
	@echo "  AMI name prefix: $(AMI_NAME_PREFIX)"
	@if [ -f $(PACKER_LOG_FILE) ]; then \
		echo "  Build log: $(PACKER_LOG_FILE) (exists)"; \
	else \
		echo "  Build log: $(PACKER_LOG_FILE) (not found)"; \
	fi

.PHONY: list-ami
list-ami: ## List recent AMIs created by this project
	@echo "$(BLUE)Recent AMIs created by this project:$(NC)"
	@aws ec2 describe-images \
		--owners self \
		--filters "Name=name,Values=$(AMI_NAME_PREFIX)*" \
		--query 'Images[*].[ImageId,Name,CreationDate,State]' \
		--output table 2>/dev/null || echo "$(YELLOW)No AMIs found or AWS CLI not configured$(NC)"

# Clean targets
.PHONY: clean
clean: ami-clean ## Clean all build artifacts

.PHONY: distclean
distclean: clean ## Deep clean (remove all generated files)
	@echo "$(BLUE)Performing deep cleanup...$(NC)"
	@find . -name "*.log" -type f -delete
	@find . -name "manifest.json" -type f -delete
	@echo "$(GREEN)Deep cleanup completed!$(NC)"

# Default target
.DEFAULT_GOAL := help
