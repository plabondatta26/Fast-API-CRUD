from sqlalchemy import Column, Integer, String
from config.database import Base


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)