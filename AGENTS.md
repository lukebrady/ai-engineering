# Repository Guidelines

## Project Structure & Modules

- `agents/` – Python agents (`oss-agent/`, `smolagent/`, `tofumatic/`), each with `pyproject.toml` and a `main.py` entrypoint.
- `infrastructure/ai-inference/` – Cloud infra: `packer/` (AMI build), `opentofu/` (`iam/`, `inference/`, reusable `modules/`).
- `infrastructure/temporal/` – Temporal stack via Docker Compose.
- `docker/` – Auxiliary containers (e.g., Chromium).
- `Makefile` – Single executable catalog of tools (`make help`).

## Build, Test, and Development Commands

- Discover tools: `make help` (grouped by AMI, Agents, Temporal, OpenTofu).
- Setup & checks: `make setup`, `make check-prerequisites`, `make check-aws-config`.
- AMI build: `make ami-build` (runs `packer init`/`validate` + build).
- Infra validate/plan/apply: `make tofu-validate`, `make tofu-plan`, `make tofu-apply`.
- Temporal stack: `make temporal-up` / `temporal-down`.
- Agents (OSS example): `make agent-oss-install` (uv sync), `make agent-oss-run`.
  - Or directly: `cd agents/oss-agent && uv sync && python main.py`.

## Coding Style & Naming Conventions

- Python (3.13): PEP 8, 4-space indent, type hints required; `snake_case` for functions/vars, `PascalCase` for classes; modules lowercase.
- IaC (HCL): run `tofu fmt`; keep modules small, input variables explicit, outputs documented.
- Shell: `bash -euo pipefail`; guard commands and check exits.
- Go (tests): `gofmt`/`go vet` if adding Go code.
- Filenames: descriptive, kebab- or snake-case (e.g., `provision.sh`, `prompt_gen.py`).

## Testing Guidelines

- Packer: `cd infrastructure/ai-inference/packer && packer validate .`.
- OpenTofu: `tofu validate` and `tofu plan` before apply; prefer module-level validation.
- Module tests (Terratest): `cd infrastructure/ai-inference/opentofu/modules/inference/test && go test -v`.
- Agents: if adding tests, use `tests/test_*.py`; fast unit tests preferred; mock network calls.

## Commit & Pull Request Guidelines

- Conventional Commits: `feat(scope): ...`, `fix(scope): ...`, `docs: ...` (scopes: `inference`, `iam`, `agents`, `temporal`).
- PRs must include: clear description, linked issues, affected paths, commands run (e.g., `tofu plan` output), and any logs/screenshots.
- Update `Makefile` when adding runnable tools; keep help text succinct.

## Security & Configuration Tips

- Never commit secrets: use `.env`, `.env.secure`, and `secure.tfvars` (referenced by targets).
- Required envs/examples: `API_ENDPOINT` (agents), AWS credentials/profile, `HUGGING_FACE_TOKEN` for tests.
- Prefer least-privilege IAM and region/instance overrides via `AWS_REGION`, `INSTANCE_TYPE`.

## Agent-Specific Instructions

- New agent layout: `agents/<name>/` with `pyproject.toml`, `main.py`, and `uv.lock`.
- Add Make targets `agent-<name>-install|run|check` mirroring `oss-agent` patterns.
