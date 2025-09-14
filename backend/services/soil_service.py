def analyze_soil(moisture: float, temperature: float, ec: float) -> dict:
    analysis = {}

    # Moisture analysis
    if moisture < 30:
        analysis["moisture"] = "Soil is too dry"
    elif 30 <= moisture <= 60:
        analysis["moisture"] = "Soil moisture is optimal"
    else:
        analysis["moisture"] = "Soil is too wet"

    # Temperature analysis
    if temperature < 15:
        analysis["temperature"] = "Soil is too cold"
    elif 15 <= temperature <= 30:
        analysis["temperature"] = "Temperature is optimal"
    else:
        analysis["temperature"] = "Soil is too hot"

    # EC (Electrical Conductivity) analysis
    if ec < 1:
        analysis["ec"] = "Low fertility"
    elif 1 <= ec <= 3:
        analysis["ec"] = "Optimal fertility"
    else:
        analysis["ec"] = "High salinity"

    return analysis

