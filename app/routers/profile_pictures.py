import io
from fastapi import APIRouter, status, UploadFile
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaIoBaseUpload
from app.models import profile_pictures_model
from .. import config
from ..dependencies import Dependencies, common_deps
from ..utils import generic_operations


router = APIRouter(prefix="/profile_pictures", tags=["Profile pictures"])

credentials_path = config.settings.google_json_credentials_path
credentials = service_account.Credentials.from_service_account_file(credentials_path)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_profile_picture(file_in: UploadFile, params: common_deps):
    drive_service: Resource = build("drive", "v3", credentials=credentials)
    file_metadata = {"name": file_in.filename}
    file_content = await file_in.read()

    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype="image/jpeg")
    uploaded_file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_id = uploaded_file["id"]
    return await profile_pictures_model.ProfilePicture.create_profile_picture(
        file_id, params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_profile_picture(params: common_deps):
    profile_picture = await generic_operations.get_item()
