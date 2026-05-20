from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_logs():
    return {"message": "Logs API is ready"}