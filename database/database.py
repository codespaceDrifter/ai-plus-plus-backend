from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATABASE_URL = f"sqlite:///{ROOT_DIR/'data'/'database.db'}?journal_mode=WAL"


engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False},
)

Base = declarative_base()
