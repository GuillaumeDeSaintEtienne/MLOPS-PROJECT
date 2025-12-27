from fastapi import APIRouter, HTTPException
from Backend.app.schemas import CreditScoreInput
from Backend.app.model_service import make_prediction

router = APIRouter()

@router.post("/predict")
def predict_score(data: CreditScoreInput):
    try:
        prediction = make_prediction(data)
        return {"credit_score": str(prediction)} 
        
    except Exception as e:
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))