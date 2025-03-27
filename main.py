import uvicorn
from alembic import command
from alembic.config import Config

from src.application.core.config import settings
from src.application.core.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        logger.error(f"Failed to apply migrations: {str(e)}", exc_info=True)

    uvicorn.run(
        "src.application.api.app:create_app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug,
        factory=True,
    )
