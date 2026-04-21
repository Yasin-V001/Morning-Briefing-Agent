import asyncio
from app.services.weather_service import fetch_weather_summary


async def main():
    result = await fetch_weather_summary()
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())