# Scripts Directory

This directory contains shell scripts used by Packer to provision the Ubuntu 24.04 AI Inference AMI.

## Files

### `provision.sh`
The baseline provisioning script that provides a minimal working foundation for AI inference workloads.

## Features

### **Baseline System Setup**
- Updates and upgrades system packages
- Installs essential tools (git, curl)
- Installs uv (modern Python package manager)
- Basic system cleanup

### **What's Included**
- **Git**: For version control and code management
- **uv**: Fast Python package manager and project management tool
- **Updated System**: Latest security patches and package versions

### **What's NOT Included (for iteration)**
- Python packages (numpy, pandas, etc.)
- Development tools (cmake, build-essential)
- Text editors or utilities
- Complex configurations
- AI-specific directories

## Design Philosophy

This script follows the **"start simple, iterate fast"** approach:

1. **Baseline First**: Get a working foundation
2. **Minimal Dependencies**: Only essential tools
3. **Easy to Extend**: Simple structure for adding features
4. **Fast Builds**: Quick iteration cycles

## Usage

The script is automatically executed by Packer during the AMI build process. It can also be run manually for testing:

```bash
# Make executable (if not already)
chmod +x provision.sh

# Run the script
./provision.sh
```

## Customization

To add features to the baseline:

1. **Add new packages**: Edit the `install_essentials()` function
2. **Add new tools**: Create new functions and call them in `main()`
3. **Add configurations**: Extend the script with new functionality

## Example: Adding Python Packages

```bash
# Add this function to provision.sh
install_python_packages() {
    log "Installing Python packages..."
    
    # Use uv to install packages
    uv pip install numpy pandas scipy
    
    log "Python packages installed successfully"
}

# Then call it in main():
# install_python_packages
```

## Logging

The script provides simple, timestamped logging:
- Blue timestamps for easy identification
- Clear progress messages
- Success confirmations

## Error Handling

The script includes basic error handling:
- Exits on any error (`set -e`)
- Undefined variable protection (`set -u`)
- Pipe failure detection (`set -o pipefail`)

## Dependencies

The script requires:
- Ubuntu 24.04 or compatible system
- Internet connectivity for package downloads
- Sudo privileges for system configuration

## Next Steps

Once you have this baseline working:

1. **Test the AMI**: Ensure git and uv work correctly
2. **Add Python packages**: Use uv to install numpy, pandas, etc.
3. **Add AI frameworks**: Install PyTorch, TensorFlow, etc.
4. **Add development tools**: Install editors, debuggers, etc.
5. **Optimize**: Add GPU drivers, performance tuning, etc.

## Why This Approach?

- **Faster builds**: Less to install = faster iteration
- **Easier debugging**: Fewer moving parts
- **Better testing**: Can test each addition independently
- **More flexible**: Easy to customize for different use cases
