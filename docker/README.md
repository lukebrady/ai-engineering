# Docker Containers

This directory contains generic, reusable Docker containers for the AI Engineering project.

## Available Containers

### [Chromium](./chromium/)

A lightweight, Alpine-based Chromium container for web automation and scraping.

- **Base Image**: Alpine Linux 3.19
- **Size**: ~150MB
- **Use Cases**: Web scraping, automated testing, PDF generation, headless browsing
- **Features**: Headless mode, GUI mode with VNC, Python automation tools

**Quick Start:**
```bash
# Build the image
docker build -t ai-engineering/chromium docker/chromium/

# Run headless Chromium
docker run -p 9222:9222 ai-engineering/chromium
```

## Design Principles

### Generic Containers
These containers are designed to be:
- **Reusable** across different projects and agents
- **Lightweight** using Alpine Linux where possible
- **Secure** running as non-root users
- **Well-documented** with comprehensive READMEs
- **Flexible** with configurable entrypoints

### Security Best Practices
- Non-root user execution
- Minimal package installation
- Read-only filesystem support
- Health checks for monitoring
- Secure defaults

### Container Organization

```
docker/
├── README.md              # This file
└── chromium/             # Generic Chromium browser
    ├── Dockerfile
    ├── .dockerignore
    ├── entrypoint.sh
    └── README.md
```

## Future Containers

Planned additions:
- **PostgreSQL** - Database container for development
- **Redis** - Caching and message broker
- **Selenium Grid** - Distributed browser testing
- **Playwright** - Modern web automation
- **Node.js** - JavaScript runtime environment

## Usage Patterns

### With Docker Compose

```yaml
version: '3.8'
services:
  chromium:
    build: ./docker/chromium
    ports:
      - "9222:9222"
    volumes:
      - ./scripts:/home/chromium/scripts
```

### In Agents

```python
# Python agent using Chromium container
import docker

client = docker.from_env()
container = client.containers.run(
    'ai-engineering/chromium',
    ports={'9222/tcp': 9222},
    detach=True
)
```

### For Development

```bash
# Interactive development
docker run -it ai-engineering/chromium shell

# Mount local code
docker run -v $(pwd):/workspace ai-engineering/chromium python /workspace/script.py
```

## Building All Containers

```bash
# Build all containers from project root
make docker-build-all

# Or individually
docker build -t ai-engineering/chromium docker/chromium/
```

## Contributing

When adding new containers:

1. **Create directory structure**:
   ```
   docker/<container-name>/
   ├── Dockerfile
   ├── .dockerignore
   ├── entrypoint.sh (if needed)
   └── README.md
   ```

2. **Follow naming conventions**:
   - Directory: lowercase with hyphens
   - Image tag: `ai-engineering/<name>`
   - User: match the service name

3. **Security requirements**:
   - Use Alpine Linux when possible
   - Run as non-root user
   - Include health checks
   - Minimize installed packages

4. **Documentation**:
   - Comprehensive README.md
   - Usage examples
   - Environment variables table
   - Common use cases

5. **Testing**:
   - Test basic functionality
   - Test security (non-root execution)
   - Test health checks
   - Verify minimal size

## Integration

These containers integrate with:
- **Agents** (`/agents/`) - Used by Python agents for browser automation
- **Infrastructure** (`/infrastructure/`) - Referenced in docker-compose files
- **CI/CD** (`.github/workflows/`) - Built and tested in pipelines

## Makefile Integration

Add container commands to the main Makefile:

```makefile
# Docker commands
.PHONY: docker-build-chromium
docker-build-chromium: ## Build Chromium container
	docker build -t ai-engineering/chromium docker/chromium/

.PHONY: docker-build-all
docker-build-all: docker-build-chromium ## Build all containers
```