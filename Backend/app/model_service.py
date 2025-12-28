import joblib
import pandas as pd
from pathlib import Path

_model = None

def load_model():
    global _model
    model_path = Path("Backend/app/model/best_model.joblib") 
    
    if model_path.exists():
        _model = joblib.load(model_path)
        print(f"✅ Model loaded from {model_path}")
    else:
        print(f"⚠️ Warning: Model file not found at {model_path}")

def make_prediction(input_data):
    if _model is None:
        raise Exception("Model is not loaded.")
    
    data_dict = input_data.dict()
    
    data_dict["Num_Credit_Card"] = data_dict.pop("Num_Credit_Cards")
    
    data_dict["Credit_History_Months"] = data_dict.pop("Credit_History_Age")

    data_dict["Month"] = "January"      
    data_dict["Occupation"] = "Other"    
    
    input_df = pd.DataFrame([data_dict])
    
    result = _model.predict(input_df)
    return result[0]