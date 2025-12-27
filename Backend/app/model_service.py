import joblib
import pandas as pd
from pathlib import Path

# We store the model in a global variable
_model = None

def load_model():
    """Loads the model from the file system."""
    global _model
    model_path = Path("best_model.joblib") # Docker works from /app, so this path is correct
    
    if model_path.exists():
        _model = joblib.load(model_path)
        print(f"✅ Model loaded from {model_path}")
    else:
        print(f"⚠️ Warning: Model file not found at {model_path}")

def make_prediction(input_data):
    """Takes a Pydantic schema, converts to DataFrame, and predicts."""
    if _model is None:
        raise Exception("Model is not loaded.")
    
    # Convert Pydantic object to DataFrame (one row)
    input_df = pd.DataFrame([input_data.dict()])
    
    # Predict
    result = _model.predict(input_df)
    return result[0]