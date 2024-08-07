#!usr/bin/env python3

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.resolve()
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)


# 并行进程数
workers = int(os.getenv("SRV_WORKERS", 1))

# 指定每个工作的线程数
threads = int(os.getenv("SRV_WORKERS_THREADS", 1))

# 最大并发量
worker_connections = int(os.getenv("SRV_WORKERS_CONNECTIONS", 1000))

# 工作模式协程
worker_class = 'uvicorn.workers.UvicornWorker'

# 监听端口
host = os.getenv('SRV_HOST', '0.0.0.0')
port = os.getenv('SRV_PORT', '8000')
bind = f'{host}:{port}'

# worker 空闲超时时间 （超时进程会被kill restart）
timeout = int(os.getenv('SRV_REQUEST_TIMEOUT', 600))

# 进程文件
pidfile = './gunicorn.pid'

if not os.path.exists("./logs/gunicorn/"):
    os.makedirs("./logs/gunicorn/")
# 访问日志和错误日志
access_log_format = '%(h)s %(l)s %(u)s "%(t)s" "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%(T)s" "%({X-Real-IP}i)s"'
accesslog = './logs/gunicorn/access.log'
errorlog = './logs/gunicorn/error.log'

# 日志级别
loglevel = 'warning'