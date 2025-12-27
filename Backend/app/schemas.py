from pydantic import BaseModel

class CreditScoreInput(BaseModel):
    Age: float
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Num_Bank_Accounts: int
    Num_Credit_Cards: int
    Interest_Rate: int
    Num_of_Loan: int
    Delay_from_due_date: int
    Num_of_Delayed_Payment: int
    Changed_Credit_Limit: float
    Num_Credit_Inquiries: float
    Credit_Mix: int 
    Outstanding_Debt: float
    Credit_History_Age: float
    Payment_of_Min_Amount: int 
    Total_EMI_per_month: float
    Amount_invested_monthly: float
    Payment_Behaviour: int 
    Monthly_Balance: float