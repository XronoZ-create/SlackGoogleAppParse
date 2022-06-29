from sqlalchemy import Column, Integer, String
from db import Base, SessionLocal

class GoogleApp(Base):
    __tablename__ = 'google_app'
    id = Column(Integer, primary_key=True)
    develop_href = Column(String, default="")
    app_id = Column(String, default="")

class DevelopHref(Base):
    __tablename__ = 'develop_id'
    id = Column(Integer, primary_key=True)
    develop_href = Column(String, default="")
    count_parse = Column(Integer, default=0)