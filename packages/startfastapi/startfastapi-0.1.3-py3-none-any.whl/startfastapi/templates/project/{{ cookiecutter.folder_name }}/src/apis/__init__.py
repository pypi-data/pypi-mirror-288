import os
import importlib
from fastapi import APIRouter
from src.core.logger import logger

router = APIRouter()

apps = []
current_dir = os.path.abspath(os.path.dirname(__file__))
for dir_name in os.listdir(current_dir):
    tmp = os.path.join(current_dir, dir_name)
    if os.path.isdir(tmp):
        if dir_name.startswith('__'):
            continue
        try:
            app = importlib.import_module(f"src.apis.{dir_name}.views")
            router.include_router(router=app.router)
            apps.append(dir_name)
        except Exception as e:
            logger.exception(f'加载应用 {dir_name} 失败，Error: {e}')
            continue

logger.info(f'已加载应用：{apps}')