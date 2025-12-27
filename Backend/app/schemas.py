from pydantic import BaseModel

class CreditScoreInput(BaseModel):
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Num_Bank_Accounts: int
    Num_Credit_Cards: int
    Outstanding_Debt: float
    Credit_History_Age: float 

    # --- OPTIONAL / DEFAULTS (Hidden) ---    
    Age: float = 30.0
    Interest_Rate: int = 15
    Num_of_Loan: int = 3
    Type_of_Loan: str = "Not Specified"
    Delay_from_due_date: int = 15
    Num_of_Delayed_Payment: int = 10
    Changed_Credit_Limit: float = 10.0
    Num_Credit_Inquiries: float = 5.0
    
    # [!] These caused the crash. Changed from Int to String:
    Credit_Mix: str = "Standard"                
    Payment_of_Min_Amount: str = "No"           
    Payment_Behaviour: str = "Low_spent_Small_value_payments" 
    
    Credit_Utilization_Ratio: float = 30.0
    Total_EMI_per_month: float = 100.0
    Amount_invested_monthly: float = 100.0
    Monthly_Balance: float = 300.0