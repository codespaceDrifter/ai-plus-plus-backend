from .database import Base
from .database import engine
from .crud import session
from .models import User, Chat, Message
from . import select

Base.metadata.create_all (engine)