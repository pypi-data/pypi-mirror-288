from src.core.app import Application
from src.core.config import settings

app = Application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        host=settings.SRV_HOST,
        port=settings.SRV_PORT,
        workers=settings.SRV_WORKERS,
        log_config=None,
        reload=True
    )