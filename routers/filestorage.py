from typing import Annotated

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session

from config.database import get_session
from decorators.auth import validate_login
from models.auth import User
from models.filestorage import CloudProvider, UserFiles, UserStorage
from schemas.filestorage import UserStats
from services.filestorage import FileService, StorageService
from services.user import UserStorageService

file_storage_router = APIRouter(prefix="/fs", tags=["File Storage"])


@file_storage_router.post("/file/", dependencies=[Depends(validate_login)])
def upload(
    request: Request,
    file_path: str,
    file_name: str,
    file: Annotated[UploadFile, File()],
    session: Session = Depends(get_session),
):
    user = request.state.user
    file_info = FileService().parse_file(file_path=file_path, file_name=file_name, file=file)

    reachs_limit = UserStorageService().validate_storage_limit(
        user=user, file_size=file_info.file_size, session=session
    )

    if reachs_limit:
        return JSONResponse(content="Limit storage reached: " + str(user.max_storage_size_mb) + "MB")

    if UserStorageService().file_exists(file=file_info, session=session):
        return JSONResponse(content="File path already exists", status_code=400)

    file_info.file_path = "/" + user.user + "/" + file_info.file_path

    result_cloud: UserFiles = StorageService().upload_file(
        file=file_info, user_id=user.id
    )

    result_db: UserFiles = UserStorageService().save_user_file_metadata(
        user_file=result_cloud, session=session
    )

    return JSONResponse(
        content=jsonable_encoder({"file_size": result_db.file_size}), status_code=200
    )


@file_storage_router.get("/stats/", dependencies=[Depends(validate_login)])
def stats(request: Request, session: Session = Depends(get_session)):
    user: User = request.state.user
    if not (user.is_admin):
        return JSONResponse(content={}, status_code=403)

    storage_per_user_cloud: list[(UserStorage, CloudProvider)] = (
        UserStorageService().get_storage_per_user(session)
    )
    stats = list(
        map(
            lambda x: UserStats(
                user_id=x[0].user_id,
                cloud_provider_id=x[0].cloud_provider_id,
                cloud_provider_name=x[1].name,
                occupied_size=x[0].occupied_size,
            ),
            storage_per_user_cloud,
        )
    )

    return JSONResponse(content=jsonable_encoder(stats), status_code=200)
