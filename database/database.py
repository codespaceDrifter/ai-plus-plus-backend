from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from .models.users import User

DATABASE_URL = "sqlite:///database.db ? journal_mode=WAL"

engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False},
)

Base = declarative_base()

Base.metadata.create_all (engine)
Session = sessionmaker(
  autoflush=False,
  autocommit=False,
  bind=engine
)

session = Session()

user = User(name="John", age=30)
user2 = User(name="Jane", age=25)
user3 = User(name="Jim", age=35)

users = session.query(User).all()

print(users[0])

session.commit()
