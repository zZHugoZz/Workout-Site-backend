from fastapi import APIRouter


router = APIRouter(prefix="/websocket", tags=["WebSockets"])


@router.websocket(path="/")
def connection():
    pass
