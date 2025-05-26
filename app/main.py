# app/main.py
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# import jwt
# from datetime import datetime, timedelta
# import httpx
# from typing import Dict, List
# from dotenv import load_dotenv
# import os
# from app.routers.product_routes import router as product_router
# from app.utils import decode_jwt


# import os
# from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.utils import decode_jwt
from app.routers.tecnico import router as tecnico_router
from app.routers.obtenerEmpresaRol import router as obtener_empresa_rol_router


# load_dotenv()

# raw = os.getenv("CORS_ORIGINS", "")
# origins = [o.strip() for o in raw.split(",") if o.strip()]

# Instanciar FastAPI
app = FastAPI(
    title="API de SIGII",
    version="0.5.0",
    description="Backend SIGII",
    dependencies=[Depends(decode_jwt)]
)

app.include_router(tecnico_router)
app.include_router(obtener_empresa_rol_router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins or ["*"],   # si no hay nada en .env, permite todos
#     allow_credentials=True,
#     allow_methods=["GET","POST","PUT"],
#     allow_headers=["*"]
# )

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



