from fastapi import APIRouter

from app.services.external_service import get_weather_sync, get_weather_async

router = APIRouter(prefix="/external", tags=["External API Simulation"])


@router.get("/weather-sync")
def weather_sync():
    return get_weather_sync()


@router.get("/weather-async")
async def weather_async():
    return await get_weather_async()