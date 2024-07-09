from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router
from contextlib import asynccontextmanager
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(title="HotelMe", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(pages_router)
app.include_router(images_router)
