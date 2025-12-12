from fastapi import Body, FastAPI, responses, status, HTTPException, Depends
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .schemas.schemas import PostCreate,PostResponse,UserCreate,UserResponse
from .models import models
from .database.database import engine, get_db
from app.utils.utils import hash_password
from app.routers import posts,users,auth



# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# PostgreSQL (psycopg2) connection loop
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastAPI",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

# ROOT ROUTE
@app.get("/")
async def read_root():
    return {"Hello": "World"}
