# backend/models/soil_model.py
from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime
from backend.core.database import Base

class SoilReading(Base):
    __tablename__ = "soil_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    ec = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

