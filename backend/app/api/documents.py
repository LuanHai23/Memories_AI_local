from fastapi import APIRouter

# Router cho nhóm API doc
router = APIRouter()

@router.get("/")
def list_documents():
    return {"message": "Documents API is ready"}

