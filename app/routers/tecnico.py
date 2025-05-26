from fastapi import APIRouter
from app.utils import require_role
from app.schemas.metadata import MetadataRead

router = APIRouter(prefix="/tecnico", tags=["metadata"], dependencies=[require_role(["BODEGA"])])

@router.post(
    "/", 
    response_model=MetadataRead, 
    status_code=201)

def create_metadata():
    print("Creating metadata...")
#     return []

