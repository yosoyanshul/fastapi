from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.schema import ForeignKey
from .database import Base

class Posts(Base):
    __tablename__ = "posts" 

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_on = Column(TIMESTAMP(timezone=true), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey ("users.id", ondelete="CASCADE"), nullable= False)
    raj_sir = Column(Integer, nullable=True)

    owner = relationship("Users")

class Users(Base): 
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=true), nullable=False, server_default=text('now()'))  


class Vote(Base):
    __tablename__ = "vote"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=true)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=true)