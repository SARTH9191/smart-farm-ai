# backend/tests/test_soil.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_and_get_soil_reading():
    # Create
    response = client.post("/soil/readings/", params={
        "sensor_id": "sensor_1",
        "moisture": 23.5,
        "temperature": 30.1,
        "ec": 1.2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == "sensor_1"

    # Read
    response = client.get("/soil/readings/")
    assert response.status_code == 200
    readings = response.json()
    assert len(readings) > 0

