from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from src.apis import router
from src.core.config import settings
from src.core.db import init_tables, close_all_session
from src.middlewares.handle_request import HandleRequestMiddleWare


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tables()
    yield
    await close_all_session()


class Application(FastAPI):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(
            debug=settings.API_DEBUG,
            lifespan=lifespan,
            *args, **kwargs
        )
        self.register_exception()
        self.register_middleware()
        self.register_router()

    def register_router(self: FastAPI) -> None:
        self.include_router(router, prefix="/api")

    def register_exception(self: FastAPI) -> None:
        pass

    def register_middleware(self: FastAPI) -> None:
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )
        self.add_middleware(HandleRequestMiddleWare)
