from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    type = Column(String)  # например: "Кемпинг", "Музей" и т.д.
    image_url = Column(String)
    contacts = Column(String)
    code = Column(String, unique=True)
    bitrix_id = Column(String, unique=True)
    created_at = Column(String)
    modified_at = Column(String) 