from database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
 __tablename__ = 'books'

 id = Column(Integer, primary_key=True, index=True, autoincrement=True)
 title = Column(String)
 author = Column(String)
 category = Column(String)
 rating = Column(Integer, default=1)