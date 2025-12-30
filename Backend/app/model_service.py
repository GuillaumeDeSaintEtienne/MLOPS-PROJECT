import joblib
import pandas as pd
import boto3
import os
from pathlib import Path

_model = None

# --- Configuration S3 ---
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_MODEL_KEY = "models/best_model.joblib"
LOCAL_MODEL_PATH = Path("Backend/app/model/best_model.joblib")

def download_model_from_s3():
    """Télécharge le fichier .joblib depuis S3 vers le dossier local"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'eu-west-3')
    )
    
    try:
        # Créer le dossier local s'il n'existe pas
        LOCAL_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 Téléchargement du modèle : s3://{BUCKET_NAME}/{S3_MODEL_KEY}...")
        s3_client.download_file(BUCKET_NAME, S3_MODEL_KEY, str(LOCAL_MODEL_PATH))
        print("✅ Modèle récupéré avec succès depuis S3.")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement S3 : {e}")
        return False

def load_model():
    global _model
    
    download_model_from_s3()
    
    if LOCAL_MODEL_PATH.exists():
        _model = joblib.load(LOCAL_MODEL_PATH)
        print(f"✅ Modèle chargé en mémoire depuis {LOCAL_MODEL_PATH}")
    else:
        print(f"⚠️ Erreur critique : Fichier modèle introuvable à {LOCAL_MODEL_PATH}")

def make_prediction(input_data):
    if _model is None:
        raise Exception("Model is not loaded.")
    
    data_dict = input_data.dict()
    data_dict["Num_Credit_Card"] = data_dict.pop("Num_Credit_Cards")
    data_dict["Credit_History_Months"] = data_dict.pop("Credit_History_Age") * 12
    
    input_df = pd.DataFrame([data_dict])
    result = _model.predict(input_df)

    return result[0]

