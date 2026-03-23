from fastapi import APIRouter, Depends, UploadFile, File
from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.exceptions import FileTooLargeException, InvalidFileTypeException
import os
import uuid

router = APIRouter()

@router.post("/upload/file", summary="通用文件上传")
def upload_file(
    file: UploadFile = File(...),
    file_type: str = "common",
    current_user = Depends(get_current_user)
):
    """
    通用文件上传接口
    - file_type: 上传文件类型 avatar/resume/logo/common
    """
    # 检查文件大小
    file_size = 0
    contents = file.file.read()
    file_size = len(contents)
    file.file.seek(0)

    if file_size > settings.MAX_FILE_SIZE:
        raise FileTooLargeException()

    # 检查文件类型
    ext = os.path.splitext(file.filename)[1].lower()[1:]
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise InvalidFileTypeException()

    # 生成保存路径
    save_dir = os.path.join(settings.UPLOAD_DIR, file_type)
    os.makedirs(save_dir, exist_ok=True)
    file_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(save_dir, file_name)

    # 保存文件
    with open(save_path, "wb") as f:
        f.write(contents)

    # 返回访问路径
    return {
        "file_url": f"/uploads/{file_type}/{file_name}",
        "file_name": file.filename,
        "file_size": file_size
    }
