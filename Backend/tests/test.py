import pytest
import joblib
import pandas as pd
from pathlib import Path

class RealInput:
    def dict(self):
        return {
            "Annual_Income": 50000.0,
            "Monthly_Inhand_Salary": 4000.0,
            "Num_Bank_Accounts": 2,
            "Outstanding_Debt": 1000.0,
            "Num_Credit_Cards": 3,      
            "Credit_History_Age": 5.0   
        }

def test_real_prediction_flow():

    model_path = Path("Backend/app/model/best_model.joblib")
    
    if not model_path.exists():
        pytest.fail(f"⚠️ Model file not found at {model_path}")
        
    model = joblib.load(model_path)
    print(f"\n✅ Model loaded successfully.")

    user_input = RealInput()
    data = user_input.dict()
    
    data["Num_Credit_Card"] = data.pop("Num_Credit_Cards")
    
    years = data.pop("Credit_History_Age")
    data["Credit_History_Months"] = years * 12 

    cols = ['Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 
            'Outstanding_Debt', 'Num_Credit_Card', 'Credit_History_Months']
    
    df_input = pd.DataFrame([data])
    df_input = df_input[cols] 

    result = model.predict(df_input)
    prediction_value = result[0]

    print(f"Prediction Result: {prediction_value}")

    assert isinstance(prediction_value, str) and prediction_value == "Standard"