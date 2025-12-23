import pandas as pd
import numpy as np
import re
from pathlib import Path

# --- Configuration des chemins ---
DATA_DIR = Path("src/data/datasets")
FILES_TO_PROCESS = {
    "train": DATA_DIR / "train.csv",
    "test": DATA_DIR / "test.csv"
}

def to_nan_placeholders(series):
    """Identifie les bruits textuels et les transforme en NaN."""
    placeholders = ['_', '_______', 'NA', 'na', '', ' ', '!@9#%8', '-', 'NaN', 'nan', 'None']
    s = series.copy().replace(placeholders, np.nan)
    return s.replace(r'^[\s_]*$', np.nan, regex=True)

def clean_numeric(series):
    """Nettoyage strict des colonnes numériques (suppression de __ et symboles)."""
    s = to_nan_placeholders(series)
    if s.dtype == 'object':
        s = s.astype(str).str.replace(r'[^\d.-]', '', regex=True).replace('', np.nan)
    return pd.to_numeric(s, errors='coerce')

def credit_history_to_months(series):
    """Transformation de l'ancienneté de crédit en valeur numérique (mois)."""
    s = to_nan_placeholders(series)
    years = s.str.extract(r'(\d+)\s*Years?', expand=False).astype(float)
    months = s.str.extract(r'(\d+)\s*Months?', expand=False).astype(float)
    return (years.fillna(0) * 12 + months.fillna(0)).replace(0, np.nan)

def clean_dataset(df):
    """Orchestration du nettoyage avec suppression des lignes corrompues."""
    df = df.copy()
    
    ids_to_drop = ['ID', 'Customer_ID', 'Name', 'SSN']
    df = df.drop(columns=[c for c in ids_to_drop if c in df.columns])
    
    if 'Payment_Behaviour' in df.columns:
        df['Payment_Behaviour'] = df['Payment_Behaviour'].str.replace('_', ' ')
        df['Payment_Behaviour'] = to_nan_placeholders(df['Payment_Behaviour'])
        df = df.dropna(subset=['Payment_Behaviour'])

    for col in df.select_dtypes(include='object').columns:
        if col != 'Payment_Behaviour':
            df[col] = to_nan_placeholders(df[col])
            df[col] = df[col].astype(str).str.replace('_', '').str.strip()

    numeric_cols = ['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts',
                    'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date',
                    'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries',
                    'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Total_EMI_per_month',
                    'Amount_invested_monthly', 'Monthly_Balance']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = clean_numeric(df[col])

    if 'Age' in df.columns:
        df.loc[(df['Age'] < 18) | (df['Age'] > 100), 'Age'] = np.nan
    
    if 'Credit_History_Age' in df.columns:
        df['Credit_History_Months'] = credit_history_to_months(df['Credit_History_Age'])
        df.drop(columns=['Credit_History_Age'], inplace=True)

    num_vars = df.select_dtypes(include=[np.number]).columns
    df[num_vars] = df[num_vars].fillna(df[num_vars].median())
    
    cat_vars = df.select_dtypes(include=['object']).columns
    for col in cat_vars:
        df[col] = df[col].fillna(df[col].mode()[0])
        
    return df

def transform_all_data():
    """Automatisation de l'ETL pour train et test."""
    DATA_DIR.mkdir(parents=True, exist_ok=True) 

    for label, path in FILES_TO_PROCESS.items():
        if path.exists():
            print(f"Nettoyage rigoureux de {label}...")
            df_raw = pd.read_csv(path, low_memory=False)
            df_cleaned = clean_dataset(df_raw)
            
            output_path = DATA_DIR / f"cleaned_{label}.csv"
            df_cleaned.to_csv(output_path, index=False)
            print(f"Fichier final sauvegardé : {output_path}")

if __name__ == "__main__":
    transform_all_data()