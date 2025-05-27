#tecnico.py

from fastapi import APIRouter
from app.utils import require_role

router = APIRouter(prefix="/tecnico", tags=["Tecnico"], dependencies=[require_role(["tecnico"])])

@router.post(
    "/", 
    # response_model=MetadataRead, 
    status_code=201)

def create_solicitud():
    print("Creating metadata...")
#     return []

