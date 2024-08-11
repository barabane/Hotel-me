from datetime import date

from pydantic import BaseModel


class SchemaHotels(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: int


class SchemaHotelsDateFromTo(BaseModel):
    date_from: date
    date_to: date
