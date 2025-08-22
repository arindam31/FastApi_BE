
import httpx
import logging

from fastapi import FastAPI
from config_loader import ConfigLoader


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Load config once at startup
config = ConfigLoader.load()

@app.get("/api/profile/{user_id}")
async def get_profile(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            user_resp = await client.get(f"{config.users_url}/users/{user_id}")
            orders_resp = await client.get(
                f"{config.orders_url}/orders", params={"userId": user_id}
            )
        except httpx.RequestError as e:
            logger.error(f"HTTP request failed: {e}")
            return {"error": "Service unavailable"}

    if user_resp.status_code != 200:
        return {"error": "User not found"}

    return {
        "user": user_resp.json(),
        "orders": orders_resp.json()
    }