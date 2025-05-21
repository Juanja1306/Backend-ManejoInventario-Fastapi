# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
import httpx
from typing import Dict, List
from dotenv import load_dotenv
import os
from app.routers.auth import router as auth_router
from app.routers.product_routes import router as product_router



# Instanciar FastAPI
app = FastAPI(
    title="API de SIGII",
    version="0.1.0",
    description="Backend SIGII",
)

app.include_router(auth_router)
app.include_router(product_router)


# Crear tablas (solo una vez al iniciar)
# Base.metadata.create_all(bind=engine)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# # Revisar si se esta ejecutando en un thread diferente
# @app.middleware("http")
# async def log_thread_middleware(request: Request, call_next):
#     start = time.time()
#     thread_name = threading.current_thread().name
#     response = await call_next(request)
#     duration = time.time() - start
#     # Lo metemos en headers para verlo fácil en cada respuesta
#     response.headers["X-Thread-Name"] = thread_name
#     response.headers["X-Process-Time"] = f"{duration:.3f}s"
#     return response



