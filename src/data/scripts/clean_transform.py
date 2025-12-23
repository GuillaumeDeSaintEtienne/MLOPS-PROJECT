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

def clean_numeric_chars(value):
    """Supprime les underscores et caractères parasites des nombres."""
    if pd.isna(value):
        return np.nan
    try:
        cleaned = re.sub(r'[^0-9.-]', '', str(value))
        return float(cleaned) if cleaned != '' else np.nan
    except:
        return np.nan

def parse_history_age(value):
    """Convertit '22 Years and 9 Months' en nombre total de mois."""
    if pd.isna(value) or value == "NA":
        return np.nan
    nums = re.findall(r'\d+', str(value))
    if len(nums) == 2:
        return int(nums[0]) * 12 + int(nums[1])
    elif len(nums) == 1:
        return int(nums[0]) * 12
    return np.nan

def clean_dataframe(df, name):
    """Logique de nettoyage unique appliquée à n'importe quel DataFrame."""
    print(f"Nettoyage du dataset : {name}...")

    # 1. Suppression des colonnes d'identification 
    drop_cols = ['ID', 'Customer_ID', 'Name', 'SSN', 'Month']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # 2. Nettoyage des colonnes numériques bruitées
    num_cols_to_clean = [
        'Age', 'Annual_Income', 'Num_of_Loan', 'Num_of_Delayed_Payment', 
        'Changed_Credit_Limit', 'Outstanding_Debt', 'Num_Credit_Inquiries'
    ]
    for col in num_cols_to_clean:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric_chars)

    # 3. Traitement des valeurs aberrantes (Outliers)
    if 'Age' in df.columns:
        df.loc[(df['Age'] < 14) | (df['Age'] > 100), 'Age'] = np.nan
    
    # 4. Conversion de l'ancienneté de crédit
    if 'Credit_History_Age' in df.columns:
        df['Credit_History_Age'] = df['Credit_History_Age'].apply(parse_history_age)

    # 5. Nettoyage des chaînes de caractères (Espaces blancs)
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].str.strip()

    # 6. Imputation des valeurs manquantes
    # Numérique : Médiane / Catégoriel : Mode
    num_vars = df.select_dtypes(include=[np.number]).columns
    df[num_vars] = df[num_vars].fillna(df[num_vars].median())

    cat_vars = df.select_dtypes(include=['object']).columns
    for col in cat_vars:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    return df

def transform_all_data():
    """Orchestration du nettoyage pour train et test."""
    DATA_DIR.mkdir(parents=True, exist_ok=True) # Assure l'existence du dossier 

    for label, path in FILES_TO_PROCESS.items():
        if path.exists():
            df = pd.read_csv(path)
            cleaned_df = clean_dataframe(df, label)
            
            output_path = DATA_DIR / f"cleaned_{label}.csv"
            cleaned_df.to_csv(output_path, index=False) # Stockage final [cite: 71, 72]
            print(f"Sauvegardé : {output_path}")
        else:
            print(f"Attention : Fichier {path} introuvable.")

if __name__ == "__main__":
    transform_all_data()