from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from jose import JWTError

from app.hotels.router import get_hotel
from app.users.exceptions import TokenExpiredException
from app.utils.decode_jwt import decode_jwt

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotel)):
    return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})


@router.get("/recover")
async def recover_password_page(request: Request, access_token: str):
    if not access_token:
        raise TokenExpiredException
    try:
        payload = decode_jwt(access_token)
    except JWTError:
        raise TokenExpiredException
    expire: str = payload.get("exp")
    if (not expire) or expire < datetime.now(UTC).timestamp():
        raise TokenExpiredException
    return templates.TemplateResponse(name="recover.html", context={"request": request, "access_token": access_token})
