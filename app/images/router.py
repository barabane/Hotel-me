import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка изобр."])


@router.post("/hotels/")
async def add_image_hotel(name: int, file: UploadFile):
    img_path = f"app/static/images/{name}.webp"
    with open(img_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    process_pic.delay(img_path)
