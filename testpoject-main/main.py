"""Serve simple HTML and FastAPI/MySQL user CRUD."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from database import Base, engine
import models  # Register the users table with SQLAlchemy
from routers import user_controller

STATIC_DIR = Path(__file__).resolve().parent / "static"


def prepare_database():
    # Keep existing user data, including ages.
    # If the earlier Name+Email-only project removed the column,
    # add it back. Existing users receive age 0 until you edit them.
    inspector = inspect(engine)
    if inspector.has_table("users"):
        columns = {column["name"] for column in inspector.get_columns("users")}
        if "age" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN age INTEGER NOT NULL DEFAULT 0"))
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


app = FastAPI(title="User CRUD - FastAPI and MySQL", lifespan=lifespan)
app.include_router(user_controller)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}
