from fastapi import APIRouter, status, UploadFile


router = APIRouter(prefix="/profile_pictures", tags=["Profile pictures"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_profile_picture(file: UploadFile):
    pass
