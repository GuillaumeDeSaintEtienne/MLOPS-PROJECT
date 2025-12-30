import pandas as pd
import numpy as np
import logging
import joblib
import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# --- Configuration des chemins ---
DATA_PATH = Path("src/data/datasets/cleaned_train.csv")
MODEL_DIR = Path("src/model/models")
MODEL_PATH = MODEL_DIR / "best_model.joblib"

# --- Configuration du Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def upload_model_to_s3(local_path, bucket_name, s3_key):
    """Téléverse le fichier joblib vers S3 en utilisant les credentials d'environnement."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'eu-west-3')
    )
    
    try:
        logger.info(f"Tentative d'upload vers s3://{bucket_name}/{s3_key}...")
        s3_client.upload_file(str(local_path), bucket_name, s3_key)
        logger.info("✅ Modèle téléversé avec succès sur S3 !")
    except ClientError as e:
        logger.error(f"❌ Erreur lors de l'upload S3 : {e}")
        return False
    return True

def train_model():
    # 1. Vérification des données
    if not DATA_PATH.exists():
        logger.error(f"Erreur : Fichier de données introuvable à {DATA_PATH}")
        return

    # 2. Chargement des données
    df = pd.read_csv(DATA_PATH)
    logger.info(f"Données chargées : {df.shape[0]} lignes.")

    target = 'Credit_Score'
    if target not in df.columns:
        logger.error(f"La colonne cible '{target}' est absente du dataset.")
        return

    X = df.drop(columns=[target])
    y = df[target]

    # 3. Prétraitement
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # 4. Pipeline
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])

    # 5. Split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 6. Entraînement
    logger.info("Démarrage de l'entraînement...")
    clf.fit(X_train, y_train)

    # 7. Évaluation
    acc = accuracy_score(y_val, clf.predict(X_val))
    logger.info(f"Précision (Accuracy) : {acc:.4f}")

    # 8. Sauvegarde locale
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    logger.info(f"Modèle sauvegardé localement : {MODEL_PATH}")

    # 9. Upload S3
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    if bucket_name:
        s3_key = "models/best_model.joblib"
        upload_model_to_s3(MODEL_PATH, bucket_name, s3_key)
    else:
        logger.warning("⚠️ Variable S3_BUCKET_NAME manquante.")

if __name__ == "__main__":
    train_model()

    