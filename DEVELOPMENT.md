# DEVELOPMENT

This document is the authoritative guide for setting up, running and contributing to the project.

## Prerequisites

Install:

- Python 3.13
- Docker Desktop
- uv

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone

```bash
git clone <repository-url>
cd langgraph-mcp-playground
```

## Virtual Environment

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Environment

Create `.env`.

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=langgraph_mcp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ENDPOINT=localhost:9000
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001
MINIO_DEFAULT_BUCKET=raw-files
MINIO_SECURE=false

STORAGE_MCP_HOST=0.0.0.0
STORAGE_MCP_PORT=8001

UPLOAD_MCP_HOST=0.0.0.0
UPLOAD_MCP_PORT=8002
```

## Start Infrastructure

```bash
docker compose --env-file .env -f docker/compose.yaml up -d
```

Stop:

```bash
docker compose --env-file .env -f docker/compose.yaml down
```

Status:

```bash
docker compose --env-file .env -f docker/compose.yaml ps
```

## Infrastructure

| Service | URL |
|---|---|
| PostgreSQL | localhost:5432 |
| pgAdmin | http://localhost:5050 |
| MinIO API | http://localhost:9000 |
| MinIO Console | http://localhost:9001 |
| Redis | localhost:6380 |
| ChromaDB | http://localhost:8000 |
| Ollama | http://localhost:11434 |
| MCP Inspector | http://localhost:6274 |

## Database

Create migration:

```bash
PYTHONPATH=src uv run alembic revision --autogenerate -m "message"
```

Apply:

```bash
PYTHONPATH=src uv run alembic upgrade head
```

## Start Storage MCP

```bash
PYTHONPATH=src uv run python -m langgraph_mcp_playground.storage.server
```

## MCP Inspector

Transport: Streamable HTTP

URL:

```text
http://host.docker.internal:8001/mcp
```

Connection Type: Via Proxy

Authentication: Disabled

## MinIO

Console:

```text
http://localhost:9001
```

Default bucket:

```text
raw-files
```

## Integration Test

Run:

```bash
PYTHONPATH=src uv run python -m langgraph_mcp_playground.scripts.test_storage_mcp
```

The test validates:

1. MCP tool discovery
2. Upload
3. Metadata
4. Download
5. Delete

## Code Quality

Format:

```bash
uv run ruff format .
```

Lint:

```bash
uv run ruff check .
```

Type checking:

```bash
uv run mypy src
```

Tests:

```bash
uv run pytest
```

## Daily Workflow

1. Activate virtual environment.
2. Start Docker infrastructure.
3. Run database migrations if required.
4. Start Storage MCP server.
5. Execute integration test.
6. Develop features.
7. Run Ruff.
8. Run MyPy.
9. Run pytest.
10. Commit only after all checks pass.

## Troubleshooting

### MCP client cannot connect

- Verify Storage MCP is running.
- Verify port 8001 is available.
- Verify `/mcp` endpoint.

### MinIO upload fails

- Verify Docker containers are running.
- Verify bucket exists.
- Verify credentials in `.env`.

### MyPy errors

- Ensure the Pydantic mypy plugin is configured.
- Prefer explicit assertions for nullable SDK values.

## Git Checklist

Before every commit:

- [ ] Ruff passes
- [ ] MyPy passes
- [ ] pytest passes
- [ ] Storage integration test passes
- [ ] Docker services healthy
- [ ] Documentation updated
