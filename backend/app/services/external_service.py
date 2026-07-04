import time
import asyncio


def get_weather_sync():
    time.sleep(2)

    return {
        "city": "Nablus",
        "temperature": 22,
        "condition": "Sunny",
        "type": "sync"
    }


async def get_weather_async():
    await asyncio.sleep(2)

    return {
        "city": "Nablus",
        "temperature": 22,
        "condition": "Sunny",
        "type": "async"
    }