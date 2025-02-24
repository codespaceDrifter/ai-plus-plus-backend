from .models import User, Chat, Message
from .database import engine
from sqlalchemy.orm import Session

session = Session(engine)

user1 = User(
  sub = "123",
  name = "John Doe"
)

user2 = User(
  sub = "456",
  name = "Jane Doe"
)

session.add_all([user1, user2])
session.commit()

chat1 = Chat(
  user_id = user1.id,
  messages = [
    Message(
      core = "Hello, how are you?",
      is_user = True
    )
  ]
)

session.add_all([chat1])
session.commit()

print ("session made")

from .models import User, Chat, Message
from sqlalchemy import select

print ("selecting user")
user_query = select(User).where(User.id == 1)
user = session.execute(user_query).scalar_one()

print(user)
