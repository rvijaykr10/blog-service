from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Blog(Base):
    __tablename__='blog'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    rating = Column(Integer)
    