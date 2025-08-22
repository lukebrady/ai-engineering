#!/bin/bash
# Ubuntu 24.04 AI Inference AMI - Baseline Provisioning Script
# This script provides a minimal working baseline for AI inference workloads

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Simple logging function
log() {
    local message="$*"
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} ${message}"
}

# Function to update system packages
update_system() {
    log "Updating system packages..."
    
    # Update package lists
    sudo apt-get update
    
    # Upgrade packages
    sudo apt-get upgrade -y
    
    # Remove unnecessary packages
    sudo apt-get autoremove -y
    
    # Clean package cache
    sudo apt-get autoclean
    
    log "System packages updated successfully"
}

# Function to install essential packages
install_essentials() {
    log "Installing essential packages..."
    
    # Install git and curl
    sudo apt-get install -y git curl
    
    log "Essential packages installed successfully"
}

# Function to install uv (Python package manager)
install_uv() {
    log "Installing uv (Python package manager)..."
    
    # Install uv using the official installer
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Add uv to PATH permanently
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
    
    # Verify installation
    if command -v uv >/dev/null 2>&1; then
        log "uv installed successfully"
        uv --version
    else
        log "Warning: uv may not be in PATH yet. Try logging out and back in."
    fi
}

# Function to clean up
cleanup() {
    log "Cleaning up..."
    
    # Remove unnecessary packages
    sudo apt-get autoremove -y
    
    # Clean package cache
    sudo apt-get autoclean
    
    # Remove temporary files
    sudo rm -rf /var/lib/apt/lists/*
    sudo rm -rf /tmp/*
    sudo rm -rf /var/tmp/*
    
    # Sync filesystem
    sudo sync
    
    log "Cleanup completed"
}

# Main execution
main() {
    log "Starting Ubuntu 24.04 AI Inference AMI baseline provisioning..."
    
    update_system
    install_essentials
    install_uv
    cleanup
    
    log "Baseline provisioning completed successfully!"
    log "The system now has:"
    log "  - Updated system packages"
    log "  - Git for version control"
    log "  - uv for Python package management"
}

# Execute main function
main "$@"
