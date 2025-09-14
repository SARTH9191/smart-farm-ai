from fastapi import APIRouter
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os

router = APIRouter()

# Build absolute path to soil_data.csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "soil_data.csv")

@router.get("/analyze")
def analyze_soil(moisture: float, ec: float, temperature: float):
    """
    Train a simple ML model on soil_data.csv and predict irrigation need.
    If CSV has no 'irrigation_needed' column, auto-generate it.
    """

    # Load latest soil data
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        return {"error": f"Soil CSV not found at {CSV_PATH}. Generate data first."}

    # ✅ Ensure irrigation_needed column exists
    if "irrigation_needed" not in df.columns:
        # Rule: irrigation needed if moisture < 30
        df["irrigation_needed"] = df["moisture"].apply(lambda m: 1 if m < 30 else 0)
        df.to_csv(CSV_PATH, index=False)  # save back with new column

    # Features + Target
    X = df[["moisture", "temperature", "ec"]]
    y = df["irrigation_needed"]

    # Train lightweight model
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X, y)

    # Predict for input
    input_data = pd.DataFrame([[moisture, temperature, ec]],
                              columns=["moisture", "temperature", "ec"])
    prediction = clf.predict(input_data)[0]

    decision = "Irrigation Needed ✅" if prediction == 1 else "No Irrigation ❌"

    return {
        "decision": decision,
        "raw_prediction": int(prediction),
        "used_data_size": len(df),
        "csv_path": CSV_PATH
    }
