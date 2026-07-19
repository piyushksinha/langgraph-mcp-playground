# LangGraph MCP Playground

A production-style learning project demonstrating how to build modular AI systems using **LangGraph** and the **Model Context Protocol (MCP)**.

## Vision

This repository explores a production-oriented architecture where LangGraph orchestrates workflows while MCP servers encapsulate infrastructure and business capabilities.

## Architecture

```text
                        LangGraph
                            │
                    MultiServerMCPClient
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
   Storage MCP                          Future MCPs
   (FastMCP)                            Customer
        │                               Booking
        ▼                               Campaign
  StorageService
        │
        ▼
      MinIO
```

## Technology

- Python 3.13
- uv
- LangGraph
- LangChain
- FastMCP
- PostgreSQL
- SQLAlchemy
- Alembic
- MinIO
- Redis
- ChromaDB
- Ollama
- Ruff
- MyPy
- pytest
- Docker

## Repository Layout

```text
.
├── docker/
├── src/
│   └── langgraph_mcp_playground/
│       ├── config/
│       ├── database/
│       ├── mcp/
│       ├── models/
│       ├── repositories/
│       ├── scripts/
│       ├── services/
│       ├── storage/
│       └── upload/
├── migrations/
├── DEVELOPMENT.md
└── README.md
```

## Current Status

### Completed

- Project scaffolding
- SQLAlchemy configuration
- Alembic migrations
- Upload model
- MinIO integration
- StorageService
- Storage FastMCP server
- MultiServerMCPClient integration
- End-to-end Storage MCP validation
- Ruff and MyPy integration

### Verified Integration

The following workflow has been tested end-to-end:

```text
Python Test Script
      │
      ▼
MultiServerMCPClient
      │
      ▼
Storage MCP
      │
      ▼
StorageService
      │
      ▼
MinIO
```

Verified operations:

- Tool discovery
- Upload
- Object metadata
- Download
- Delete

## Design Principles

- LangGraph orchestrates workflows.
- MCP servers own business and infrastructure logic.
- Services remain modular and independently deployable.
- Keep orchestration separate from implementation.
- Validate integrations before adding abstractions.

## Roadmap

- MCP Gateway abstraction
- Upload metadata persistence
- CSV ingestion
- PostgreSQL MCP
- Customer MCP
- Booking MCP
- Campaign MCP
- LangGraph workflows
- Multi-agent orchestration

## Documentation

Development setup, configuration, testing and daily workflow are documented in **DEVELOPMENT.md**.

## License

MIT
