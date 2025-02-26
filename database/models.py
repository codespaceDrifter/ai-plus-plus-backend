from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True)
  sub = Column(String, nullable=False)
  name = Column(String(50), nullable=False)
  chats = relationship("Chat", back_populates="user")

class Chat(Base):
  __tablename__ = "chats"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
  messages = relationship("Message", back_populates="chat")
  user = relationship("User", back_populates="chats")

class Message(Base):
  __tablename__ = "messages"
  id = Column(Integer, primary_key=True, autoincrement=True)
  core = Column(String, nullable=False)
  is_user = Column(Boolean, nullable=False)
  chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
  chat = relationship("Chat", back_populates="messages")

