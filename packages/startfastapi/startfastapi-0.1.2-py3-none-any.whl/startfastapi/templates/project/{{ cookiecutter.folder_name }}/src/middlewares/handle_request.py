import uuid
from fastapi import Request
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from src.core.logger import logger, request_id_context


class HandleRequestMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None) -> None:
        super(HandleRequestMiddleWare, self).__init__(app, dispatch)

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_context.set(request_id)
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {request.headers}")

        if request.method in ["POST", "PUT"]:
            logger.info(f"Body: {await request.json()}")

        response = await call_next(request)
        response.headers["trace-id"] = request_id
        return response



