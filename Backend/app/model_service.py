import joblib
import pandas as pd
from pathlib import Path

_model = None

def load_model():
    global _model
    model_path = Path("Backend/best_model.joblib") 
        
    if model_path.exists():
        _model = joblib.load(model_path)
        print(f"✅ Model loaded from {model_path}")
    else:
        print(f"⚠️ Warning: Model file not found at {model_path}")

def make_prediction(input_data):
    """Takes a Pydantic schema, converts to DataFrame, and predicts."""
    if _model is None:
        raise Exception("Model is not loaded.")
    
    input_df = pd.DataFrame([input_data.dict()])
    
    result = _model.predict(input_df)
    return result[0]