import shutil

from fastapi import APIRouter, UploadFile

from core.celery_.tasks.tasks import saving_photo


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(upload_file: UploadFile):
    image_path = f"static/images/originals/{upload_file.filename}"
    with open(image_path, "wb+") as file:
        shutil.copyfileobj(upload_file.file, file)
        
    saving_photo.delay(file_path=image_path)
    return {"status": "ok"}
