"""MySQL engine and request-scoped SQLAlchemy session."""
import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

# DATABASE_URL = URL.create(
#     drivername="mysql+pymysql",
#     username=os.getenv("DB_USER", "root"),
#     password=os.getenv("DB_PASSWORD", "root"),
#     host=os.getenv("DB_HOST", "localhost"),
#     port=int(os.getenv("DB_PORT", "3306")),
#     database=os.getenv("DB_NAME", "crud_db"),
# )

# DATABASE_URL = URL.create(
#     drivername="postgresql+psycopg2",
#     username=os.getenv("DB_USER", "training_40s1_user"),
#     password=os.getenv("DB_PASSWORD", "EFWXlQkOW12BCY9k3xuwnsgbMjIkOgdJ"),
#     host=os.getenv("DB_HOST", "dpg-dbbfh8gm7kps73eqclv0-a.oregon-postgres.render.com"),
#     port=int(os.getenv("DB_PORT", "5432")),
#     database=os.getenv("DB_NAME", "training_40s1"),
# )
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "training_40s1_user"),
    password=os.getenv("DB_PASSWORD", "EFWXlQkOW12BCY9k3xuwnsgbMjIkOgdJ"),
    host=os.getenv("DB_HOST", "dpg-dbbfh9rbc2fs73b19o4g-a.virginia-postgres.render.com"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "training_40s1"),
)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db
