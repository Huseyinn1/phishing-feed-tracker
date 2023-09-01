from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    url_id = Column(Integer)
    url_author = Column(String)
    source = Column(String)  