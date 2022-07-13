from sqlalchemy import Column, Integer, String
from db import Base, SessionLocal

class GoogleApp(Base):
    __tablename__ = 'google_app'
    id = Column(Integer, primary_key=True)
    develop_href = Column(String, default="")
    app_id = Column(String, default="")

class AndroidDevelopHref(Base):
    __tablename__ = 'android_develop_id'
    id = Column(Integer, primary_key=True)
    develop_href = Column(String, default="")
    count_parse = Column(Integer, default=0)


class IosApp(Base):
    __tablename__ = 'ios_app'
    id = Column(Integer, primary_key=True)
    develop_id = Column(Integer)
    app_id = Column(Integer)

class IosDevelopHref(Base):
    __tablename__ = 'ios_develop_id'
    id = Column(Integer, primary_key=True)
    develop_id = Column(Integer)  # IOS
    count_parse = Column(Integer, default=0)
