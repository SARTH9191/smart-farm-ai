from pydantic import BaseModel, Field

class SoilCreate(BaseModel):
    moisture: float = Field(..., ge=0, le=100, description="Moisture % (0-100)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH level (0-14)")
    nutrients: str = Field(..., description="Nutrient info like NPK ratio")

class SoilResponse(SoilCreate):
    id: int
    analysis: str  # 👈 This is your contribution
    class Config:
        orm_mode = True
