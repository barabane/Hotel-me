from pydantic import BaseModel, EmailStr, ConfigDict


class SchemaUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)
