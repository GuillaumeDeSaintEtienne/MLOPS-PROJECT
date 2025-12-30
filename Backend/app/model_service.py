import joblib
import pandas as pd
from pathlib import Path

_model = None


LOCAL_MODEL_PATH = Path("Backend/app/model/best_model.joblib")

def load_model():
    """Charge le modèle déjà présent dans le container (téléchargé par le CI/CD)"""
    global _model
    
    if LOCAL_MODEL_PATH.exists():
        try:
            _model = joblib.load(LOCAL_MODEL_PATH)
            print(f"✅ Modèle chargé avec succès depuis {LOCAL_MODEL_PATH}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du fichier joblib : {e}")
    else:
        # Si le fichier manque ici, c'est que l'étape 'aws s3 cp' du workflow a échoué
        print(f"⚠️ Erreur critique : Le fichier modèle est introuvable à {LOCAL_MODEL_PATH}")
        print("Vérifiez que le workflow GitHub a bien téléchargé le modèle avant le build Docker.")

def make_prediction(input_data):
    if _model is None:
        raise Exception("Modèle non chargé. Impossible de prédire.")
    
    # Préparation des données (identique à ton code précédent)
    data_dict = input_data.dict()
    data_dict["Num_Credit_Card"] = data_dict.pop("Num_Credit_Cards")
    data_dict["Credit_History_Months"] = data_dict.pop("Credit_History_Age") * 12
    
    input_df = pd.DataFrame([data_dict])
    result = _model.predict(input_df)

    return result[0]