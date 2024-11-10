from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date


app = FastAPI()

# Модель данных пользователя
class User(BaseModel):
    id: int
    username: str
    wallet: float
    birthdate: date

# Фейковая база данных
db_users = [
    User(id=1, username="user1", wallet=100.0, birthdate=date(1990, 1, 1)),
    User(id=2, username="user2", wallet=200.0, birthdate=date(1995, 5, 15)),
]

# Корневой маршрут
@app.get("/")
async def read_root():
    return {"message": "Welcome to the User Management API!"}

# Получение списка всех пользователей
@app.get("/users/", response_model=List[User])
async def read_users():
    return db_users

# Получение пользователя по его ID
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Создание нового пользователя
@app.post("/users/", response_model=User)
async def create_user(user: User):
    db_users.append(user)
    return user

# Обновление данных пользователя
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for db_user in db_users:
        if db_user.id == user_id:
            db_user.username = user.username
            db_user.wallet = user.wallet
            db_user.birthdate = user.birthdate
            return db_user
    raise HTTPException(status_code=404, detail="User not found")

# Удаление пользователя по его ID
@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    db_user_index = next((i for i, u in enumerate(db_users) if u.id == user_id), None)
    if db_user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = db_users.pop(db_user_index)
    return deleted_user
