# Generic Chromium Docker Container

A lightweight, security-focused Docker container based on Alpine Linux providing headless Chromium browser capabilities for web automation, scraping, and testing.

## Features

- **Alpine Linux base** - Minimal footprint (~150MB vs ~1GB Ubuntu)
- **Headless Chromium** with remote debugging capabilities
- **GUI Mode** with VNC support for visual debugging
- **Security-focused** runs as non-root user
- **Web automation tools** pre-installed (Selenium, requests, BeautifulSoup)
- **Flexible entrypoint** supports multiple use cases
- **Health checks** for container monitoring

## Quick Start

### Build the Image

```bash
# From the project root
docker build -t ai-engineering/chromium docker/chromium/
```

### Basic Usage

```bash
# Run headless Chromium (default)
docker run -p 9222:9222 ai-engineering/chromium

# Access remote debugging at http://localhost:9222
```

## Usage Modes

### 1. Headless Mode (Default)

Perfect for automation and scraping:

```bash
# Basic headless mode
docker run -p 9222:9222 ai-engineering/chromium

# With custom URL
docker run -p 9222:9222 ai-engineering/chromium chromium --url=https://example.com

# With additional Chromium flags
docker run -p 9222:9222 ai-engineering/chromium chromium --window-size=1280,720
```

### 2. GUI Mode with VNC

For visual debugging and development:

```bash
# Start with VNC server
docker run -p 9222:9222 -p 5900:5900 -e ENABLE_VNC=true ai-engineering/chromium gui

# Connect to VNC at localhost:5900 (no password required)
```

### 3. Python Script Mode

Run custom Python scripts with Chromium available:

```bash
# Mount your script and run it
docker run -v $(pwd)/script.py:/home/chromium/script.py ai-engineering/chromium python script.py

# With GUI support for Selenium scripts
docker run -e GUI_MODE=true -v $(pwd)/selenium_script.py:/home/chromium/script.py ai-engineering/chromium python script.py
```

### 4. Interactive Shell

For debugging and exploration:

```bash
docker run -it ai-engineering/chromium shell
```

### 5. Custom Commands

Run any custom command in the container:

```bash
docker run ai-engineering/chromium wget -O - https://example.com
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISPLAY_NUM` | `99` | X11 display number for GUI mode |
| `VNC_PORT` | `5900` | VNC server port |
| `DEBUG_PORT` | `9222` | Chromium remote debugging port |
| `ENABLE_VNC` | `false` | Enable VNC server in GUI mode |
| `GUI_MODE` | `false` | Enable X11 for Python scripts |

## Ports

- `9222` - Chromium remote debugging interface
- `5900` - VNC server (when enabled)

## Common Use Cases

### Web Scraping

```python
# Example Python script for web scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--remote-debugging-port=9222')
driver = webdriver.Remote(
    command_executor='http://localhost:9222',
    options=options
)

driver.get('https://example.com')
print(driver.title)
driver.quit()
```

### Automated Testing

```bash
# Run headless browser for testing
docker run -d --name chromium-test -p 9222:9222 ai-engineering/chromium

# Your test scripts can connect to localhost:9222
```

### PDF Generation

```bash
# Generate PDF from webpage
docker run -v $(pwd)/output:/home/chromium/output ai-engineering/chromium \
  chromium --print-to-pdf=/home/chromium/output/page.pdf https://example.com
```

## Security Features

- Runs as non-root user (`chromium:chromium`)
- Sandboxed Chromium execution
- Minimal attack surface
- Read-only filesystem support
- Health checks for monitoring

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure the container runs as the chromium user
2. **Display Issues**: Use `GUI_MODE=true` for scripts requiring display
3. **Memory Issues**: Increase `--shm-size` for complex pages: `docker run --shm-size=2gb ...`

### Debug Mode

```bash
# Run with verbose logging
docker run -e DEBUG=true ai-engineering/chromium
```

### Check Container Health

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' <container-id>
```

## Integration Examples

### With Docker Compose

```yaml
version: '3.8'
services:
  chromium:
    build: ./docker/chromium
    ports:
      - "9222:9222"
      - "5900:5900"
    environment:
      - ENABLE_VNC=true
    volumes:
      - ./scripts:/home/chromium/scripts
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9222/json"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### In Python Applications

```python
import requests

# Connect to remote debugging API
response = requests.get('http://localhost:9222/json')
tabs = response.json()
print(f"Active tabs: {len(tabs)}")
```

## Development

### Building Locally

```bash
cd docker/chromium
docker build -t chromium-dev .
```

### Testing

```bash
# Test basic functionality
docker run --rm chromium-dev chromium --version

# Test remote debugging
docker run -d -p 9222:9222 --name test-chromium chromium-dev
curl http://localhost:9222/json
docker stop test-chromium
```

## Contributing

When modifying this container:

1. Update the Dockerfile for system-level changes
2. Update entrypoint.sh for runtime behavior
3. Update this README for documentation
4. Test all usage modes before committing

## License

Part of the AI Engineering project infrastructure.