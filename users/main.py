from fastapi import FastAPI

app = FastAPI()

USERS = {
    1: {"id": 1, "name": "Adam", "email": "adame@example.com"},
    2: {"id": 2, "name": "Eve", "email": "eve@example.com"},
}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = USERS.get(user_id)
    if not user:
        return {"error": "User not found"}
    return user