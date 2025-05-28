# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.utils import decode_jwt, require_app
from app.routers.tecnico import router as tecnico_router
from app.routers.obtenerDataUsuario import router as obtenerDataUsuario_router
from app.routers.asignarBodegas import router as asignarBodegas_router
from app.routers.producto import router as producto_router
from app.routers.bodega import router as bodega_router

# load_dotenv()

# raw = os.getenv("CORS_ORIGINS", "")
# origins = [o.strip() for o in raw.split(",") if o.strip()]

# Instanciar FastAPI
app = FastAPI(
    title="API de SIGII",
    version="0.5.0",
    description="Backend SIGII",
    dependencies=[
        Depends(decode_jwt),
        require_app("SIGII")
    ]
)

app.include_router(tecnico_router)
app.include_router(obtenerDataUsuario_router)
app.include_router(asignarBodegas_router)
app.include_router(producto_router)
app.include_router(bodega_router)




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



