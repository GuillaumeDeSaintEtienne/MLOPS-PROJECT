from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(title="Credit Score API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # À restreindre en production
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path("models/credit_score_model.joblib")
model = joblib.load(MODEL_PATH)

class CreditData(BaseModel):
    Month: float
    Age: float
    Annual_Income: float
    Num_Bank_Accounts: float
    Num_Credit_Card: float
    Interest_Rate: float
    Num_of_Loan: float
    Delay_from_due_date: float
    Num_of_Delayed_Payment: float
    Changed_Credit_Limit: float
    Num_Credit_Inquiries: float
    Outstanding_Debt: float
    Credit_Utilization_Ratio: float
    Total_EMI_per_month: float
    Amount_invested_monthly: float
    Monthly_Balance: float

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/predict")
def predict(data: CreditData):
    input_df = pd.DataFrame([data.dict()])
    
    prediction = model.predict(input_df)
    
    return {"credit_score": str(prediction[0])}