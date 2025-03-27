import uvicorn

from src.applications.config import settings
from src.applications.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    uvicorn.run(
        "src.applications.api.app:create_app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug,
        factory=True,
    )
