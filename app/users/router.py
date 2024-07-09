from fastapi import APIRouter, Depends, Response
from app.users.dependencies import get_current_user
from app.users.exceptions import UserAlreadyExistsException, UserIsNotExistsException
from app.users.models import Users
from app.users.schemas import SchemaUserAuth
from app.users.dao import UserDAO
from app.users.auth import create_access_token, get_password_hash, authenticate_user
from app.tasks.tasks import confirm_registry


router = APIRouter(
    prefix="/users",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SchemaUserAuth = Depends(SchemaUserAuth)):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    confirm_registry.delay(user_data.email)


@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserAuth = Depends(SchemaUserAuth)):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise UserIsNotExistsException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="user_access_token",
                        value=access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    return response.delete_cookie("user_access_token")


@router.get("/me")
async def get_user_me(current_user: Users = Depends(get_current_user)):
    return current_user
