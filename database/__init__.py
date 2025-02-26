from .database import Base
from .database import engine
from .models import User, Chat, Message

Base.metadata.create_all(engine)