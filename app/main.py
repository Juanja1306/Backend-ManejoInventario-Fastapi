# app/main.py

from fastapi import FastAPI

from app.models import Base
from app.database import engine, get_db
from app.routers.items import router as items_router

import time, threading
from fastapi import Request


# 1. Crear tablas (solo una vez al iniciar)
# Base.metadata.create_all(bind=engine)

# 2. Instanciar FastAPI
app = FastAPI(
    title="API de SIGII",
    version="0.1.0",
    description="Backend SIGII",
)

# 3. Montar tu router, inyectando get_db en cada endpoint
app.include_router(
    items_router,
    prefix="/api",
    tags=["SIGII"]
)




@app.middleware("http")
async def log_thread_middleware(request: Request, call_next):
    start = time.time()
    thread_name = threading.current_thread().name
    response = await call_next(request)
    duration = time.time() - start
    # Lo metemos en headers para verlo fácil en cada respuesta
    response.headers["X-Thread-Name"] = thread_name
    response.headers["X-Process-Time"] = f"{duration:.3f}s"
    return response



