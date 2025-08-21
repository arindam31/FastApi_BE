from fastapi import FastAPI
from typing import List

app = FastAPI()

ORDERS = [
    {"orderId": 101, "userId": 1, "total": 49.99},
    {"orderId": 102, "userId": 1, "total": 19.99},
    {"orderId": 201, "userId": 2, "total": 99.99},
]

@app.get("/orders")
def get_orders(userId: int) -> List[dict]:
    return [o for o in ORDERS if o["userId"] == userId]
