from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.soil_model import SoilReading
from backend.services.soil_service import analyze_soil
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
import csv
import random
import pandas as pd
from fastapi.responses import JSONResponse, FileResponse



# ---------- Router ----------
router = APIRouter(prefix="/soil", tags=["Soil"])

# ---------- CSV Setup ----------
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "soil_data.csv")

# Make sure data folder & CSV headers exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "sensor_id", "moisture", "temperature", "ec", "timestamp"])

# ---------- Pydantic Schemas ----------
class SoilCreate(BaseModel):
    sensor_id: str
    moisture: float
    temperature: float
    ec: float

class SoilResponse(BaseModel):
    id: int
    sensor_id: str
    moisture: float
    temperature: float
    ec: float
    timestamp: datetime
    analysis: dict

    class Config:
        orm_mode = True

# ---------- Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Helper: Save to CSV ----------
def save_to_csv(soil):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            soil.id,
            soil.sensor_id,
            soil.moisture,
            soil.temperature,
            soil.ec,
            soil.timestamp
        ])

# ---------- CRUD Routes ----------
@router.post("/", response_model=SoilResponse)
def create_soil_reading(reading: SoilCreate, db: Session = Depends(get_db)):
    soil = SoilReading(
        sensor_id=reading.sensor_id,
        moisture=reading.moisture,
        temperature=reading.temperature,
        ec=reading.ec,
        timestamp=datetime.utcnow(),
    )
    db.add(soil)
    db.commit()
    db.refresh(soil)

    # Save also in CSV
    save_to_csv(soil)

    return SoilResponse(
        id=soil.id,
        sensor_id=soil.sensor_id,
        moisture=soil.moisture,
        temperature=soil.temperature,
        ec=soil.ec,
        timestamp=soil.timestamp,
        analysis=analyze_soil(soil.moisture, soil.temperature, soil.ec)
    )

@router.get("/", response_model=List[SoilResponse])
def get_all_readings(db: Session = Depends(get_db)):
    readings = db.query(SoilReading).all()
    if not readings:
        raise HTTPException(status_code=404, detail="No soil readings found")
    return [
        SoilResponse(
            id=r.id,
            sensor_id=r.sensor_id,
            moisture=r.moisture,
            temperature=r.temperature,
            ec=r.ec,
            timestamp=r.timestamp,
            analysis=analyze_soil(r.moisture, r.temperature, r.ec)
        )
        for r in readings
    ]

# ---------- Auto-generate Route ----------
@router.post("/auto-generate")
def auto_generate_soil_reading(db: Session = Depends(get_db)):
    reading = SoilReading(
        sensor_id=f"SENSOR_{random.randint(1, 100)}",
        moisture=round(random.uniform(10, 60), 2),
        temperature=round(random.uniform(15, 40), 2),
        ec=round(random.uniform(0.5, 2.5), 2),
        timestamp=datetime.utcnow(),
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    # Save also in CSV
    save_to_csv(reading)

    # Analyze reading
    analysis = analyze_soil(reading.moisture, reading.temperature, reading.ec)

    return {
        "id": reading.id,
        "sensor_id": reading.sensor_id,
        "moisture": reading.moisture,
        "temperature": reading.temperature,
        "ec": reading.ec,
        "timestamp": reading.timestamp,
        "analysis": analysis,
    }

# ---------- CSV Routes ----------
@router.get("/csv")
def get_soil_csv_data():
    """
    Read soil_data.csv and return as JSON
    """
    try:
        df = pd.read_csv(CSV_FILE)
        return JSONResponse(content=df.to_dict(orient="records"))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/csv/download")
def download_soil_csv():
    """
    Download soil_data.csv file
    """
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="CSV file not found")
    return FileResponse(
        path=CSV_FILE,
        media_type="text/csv",
        filename="soil_data.csv"
    )



