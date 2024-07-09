from fastapi import APIRouter, Depends
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SchemaHotelsDateFromTo
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotel(location: str, dates=Depends(SchemaHotelsDateFromTo)):
    return await HotelDAO.find_not_empty_hotels(location, dates.date_from, dates.date_to)


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, dates=Depends(SchemaHotelsDateFromTo)):
    return await HotelDAO.find_hotel_rooms(hotel_id, dates.date_from, dates.date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_info(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)
