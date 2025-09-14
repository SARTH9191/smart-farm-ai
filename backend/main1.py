# backend/main.py
from fastapi import FastAPI
from backend.api import soil_routes, water_routes, weather_routes, blockchain_routes, lead_routes

app = FastAPI(
    title="Smart Farming System",
    description="AI-powered farming system with multiple agents",
    version="1.0.0"
)

# Register Routers
app.include_router(soil_routes.router, prefix="/soil", tags=["Soil Agent"])
app.include_router(water_routes.router, prefix="/water", tags=["Water Agent"])
app.include_router(weather_routes.router, prefix="/weather", tags=["Weather Agent"])
app.include_router(blockchain_routes.router, prefix="/blockchain", tags=["Blockchain Agent"])
app.include_router(lead_routes.router, prefix="/lead", tags=["Lead Agent"])  # 👈 MUST BE HERE

@app.get("/")
def root():
    return {"message": "🚜 Smart Farming System API running"}
