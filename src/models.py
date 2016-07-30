from . import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, Text
from sqlalchemy.orm import backref, relationship

class User(Base):
    __tablename__ = 'user'
    idx = Column(Integer, primary_key=True)
    name = Column(String(16))

class Katalk(Base):
    __tablename__ = 'kakaotalk'
    idx = Column(Integer, primary_key=True)
    unique_key = Column(String(32), unique=True)
    user_id = Column(Integer, ForeignKey("user.idx"))
    user = relationship("User", backref=backref('katalks', order_by=idx))
    text = Column(Text)
    strlength = Column(Integer)
    created_at = Column(DateTime())
    
    
    

