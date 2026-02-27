from database import Base
from sqlalchemy import Column, Integer, String, Date,VARCHAR

class BOOK(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255), nullable=False)
    author = Column(VARCHAR(255), nullable=False)
    published_date = Column(Date, nullable=True )