from sqlalchemy.orm import sessionmaker

from langgraph_mcp_playground.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)