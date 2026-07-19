# LangGraph MCP Playground

A production-style learning project for building AI applications using **LangGraph** and the **Model Context Protocol (MCP)**.

The goal is to understand how to build modular AI systems where LangGraph orchestrates workflows while individual MCP servers encapsulate infrastructure and business capabilities.

---

# Architecture

```
                        LangGraph
                            │
                            │
                (MCP Client / HTTP)
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
      Storage MCP                  Future MCP Servers
      (FastMCP)                    Customer MCP
            │                       Booking MCP
            │                       Campaign MCP
            ▼
      Storage Service
            │
            ▼
         MinIO Object Storage
```

Current implementation focuses on the **Storage MCP**.

---

# Tech Stack

- Python 3.13
- uv
- LangGraph
- LangChain
- FastMCP
- PostgreSQL 17
- SQLAlchemy
- Alembic
- MinIO
- Redis
- ChromaDB
- Ollama
- Docker
- Pydantic Settings
- Ruff
- MyPy
- pytest

---

# Project Structure

```
.
├── docker/
│   └── compose.yaml
│
├── src/
│   └── langgraph_mcp_playground/
│       ├── config/
│       ├── database/
│       ├── models/
│       ├── storage/
│       ├── graphs/
│       ├── services/
│       ├── utils/
│       └── main.py
│
├── migrations/
├── pyproject.toml
└── README.md
```

---

# Prerequisites

Install:

- Docker Desktop
- Python 3.13
- uv

Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# Clone Project

```bash
git clone <repository-url>

cd langgraph-mcp-playground
```

---

# Create Virtual Environment

```bash
uv venv

source .venv/bin/activate
```

Install dependencies

```bash
uv sync
```

---

# Environment Variables

Create:

```
.env
```

Example

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
```

---

# Start Infrastructure

Start Docker services

```bash
docker compose \
    --env-file .env \
    -f docker/compose.yaml \
    up -d
```

Verify

```bash
docker ps
```

---

# Infrastructure

| Service | URL |
|----------|-----|
| PostgreSQL | localhost:5432 |
| pgAdmin | http://localhost:5050 |
| MinIO API | http://localhost:9000 |
| MinIO Console | http://localhost:9001 |
| Ollama | http://localhost:11434 |
| ChromaDB | http://localhost:8000 |
| Redis | localhost:6380 |
| MCP Inspector | http://localhost:6274 |

---

# Database Migration

Generate migration

```bash
PYTHONPATH=src uv run alembic revision --autogenerate -m "Initial migration"
```

Run migration

```bash
PYTHONPATH=src uv run alembic upgrade head
```

---

# Run Storage MCP

Activate virtual environment

```bash
source .venv/bin/activate
```

Run server

```bash
PYTHONPATH=src uv run python \
    -m langgraph_mcp_playground.storage.server
```

The server starts using **Streamable HTTP**.

---

# MCP Inspector

The project uses the official Docker image.

Open

```
http://localhost:6274
```

## Connection Settings

Transport

```
Streamable HTTP
```

URL

```
http://host.docker.internal:8001/mcp
```

Connection Type

```
Via Proxy
```

Authentication

Disabled for local development.

---

# MinIO

Open

```
http://localhost:9001
```

Login

```
Username
minio

Password
minio123
```

Bucket

```
raw-files
```

---

# Development Workflow

Start infrastructure

```bash
docker compose \
    --env-file .env \
    -f docker/compose.yaml \
    up -d
```

Activate environment

```bash
source .venv/bin/activate
```

Run Storage MCP

```bash
PYTHONPATH=src uv run python \
    -m langgraph_mcp_playground.storage.server
```

Open Inspector

```
http://localhost:6274
```

Connect using the configuration above.

---

# Code Quality

Format

```bash
uv run ruff format .
```

Lint

```bash
uv run ruff check .
```

Type checking

```bash
uv run mypy src
```

Run tests

```bash
uv run pytest
```

---

# Current Status

Completed

- SQLAlchemy setup
- Alembic migrations
- Upload model
- MinIO integration
- Storage Service
- FastMCP Storage Server
- Streamable HTTP transport
- Dockerized MCP Inspector
- End-to-end Storage MCP connectivity

---

# Roadmap

- Upload metadata persistence
- PostgreSQL MCP
- CSV parsing workflow
- Customer MCP
- Booking MCP
- Campaign MCP
- LangGraph orchestration
- Multi-agent workflows

---

# Design Principles

- LangGraph orchestrates workflows.
- Business logic lives inside MCP servers.
- Infrastructure is accessed through MCP servers.
- MCP servers are independently deployable.
- Keep orchestration separate from implementation.

---

# License

MIT