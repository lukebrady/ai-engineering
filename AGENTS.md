## Cursor Cloud specific instructions

### Overview

This is a Python monorepo ("ai-engineering") containing AI agents, cloud infrastructure-as-code (OpenTofu/Packer), and a Temporal workflow stack. See `README.md` for full project structure and `make help` for the executable tool catalog.

### Python environment

- **Python >= 3.13** is required (`pyproject.toml`). The system default may be 3.12; Python 3.13 must be installed from `ppa:deadsnakes/ppa`.
- **uv** is the package manager. Run `uv sync` from the workspace root to install all dependencies (both main and dev).
- The virtual environment is at `.venv/`. Use `uv run <command>` to execute within it.

### Lint / Test / Build

- **Lint**: `uv run black --check .` and `uv run isort --check-only .` (formatting); `uv run mypy agents/` (type checking — note: mypy reports a duplicate-module error due to multiple `main.py` files; this is a known issue).
- **Tests**: `uv run pytest` (no test files exist yet; pytest is configured and available).
- **Run agents**: `uv run python agents/tools/tools.py` (basic hello-world); `uv run python agents/oss_agent/main.py` (requires `API_ENDPOINT` env var pointing to a vLLM server).
- All Makefile targets are documented via `make help`.

### Docker / Temporal stack

- Docker is required for the Temporal workflow stack (`infrastructure/temporal/`).
- In the cloud VM (nested Docker-in-Docker), `fuse-overlayfs` storage driver and `iptables-legacy` are needed. Start dockerd manually: `sudo dockerd &>/tmp/dockerd.log &`.
- Start Temporal: `sudo docker compose -f infrastructure/temporal/docker-compose.yml --env-file infrastructure/temporal/config.env up -d`
- Temporal UI is at `http://localhost:8080`, gRPC API at port `7233`.

### Infrastructure (OpenTofu / Packer)

These targets (`make tofu-*`, `make ami-*`) require AWS credentials and are for cloud deployment only. They are not needed for local development or testing of the agent code.
