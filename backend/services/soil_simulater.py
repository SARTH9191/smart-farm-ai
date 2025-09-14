import random
import time

def generate_soil_reading():
    return {
        "moisture": round(random.uniform(20, 80), 2),  # %
        "ph": round(random.uniform(5.5, 7.5), 2),
        "temperature": round(random.uniform(15, 35), 2),  # °C
        "nitrogen": random.randint(20, 100),  # mg/kg
        "phosphorus": random.randint(10, 50),  # mg/kg
        "potassium": random.randint(50, 200),  # mg/kg
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }