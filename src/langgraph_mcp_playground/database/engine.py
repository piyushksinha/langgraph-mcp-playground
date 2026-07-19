from sqlalchemy import create_engine

from langgraph_mcp_playground.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)