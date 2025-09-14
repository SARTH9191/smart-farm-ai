from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core import database
from backend.models import soil_model
from backend.api import soil_routes

# Create tables
soil_model.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Smart Farming System")

# --- CORS: allow frontend at localhost:3000 (CRA) or 5173 (Vite) ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------------

# Include routes
app.include_router(soil_routes.router)

@app.get("/")
def root():
    return {"message": "Smart Farming API is running 🚀"}
