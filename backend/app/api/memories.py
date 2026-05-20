from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_memories():
    return {"message": "Memories API is ready"}
