import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# --- Configuration ---
DATA_PATH = Path("src/data/datasets/cleaned_train.csv")
MODEL_DIR = Path("src/model/models")
MODEL_PATH = MODEL_DIR / "credit_score_model.joblib"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def train_model():
    if not DATA_PATH.exists():
        logger.error(f"Fichier de données introuvable : {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    logger.info(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes.")


    target = 'Credit_Score'
    if target not in df.columns:
        logger.error(f"La colonne cible '{target}' est absente du dataset.")
        return

    X = df.drop(columns=[target])
    y = df[target]

    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()

    logger.info(f"Colonnes numériques : {len(numeric_features)}")
    logger.info(f"Colonnes catégorielles : {len(categorical_features)}")


    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])


    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])


    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


    logger.info("Démarrage de l'entraînement du modèle...")
    clf.fit(X_train, y_train)


    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    logger.info(f"Précision du modèle (Accuracy) : {acc:.4f}")
    logger.info("\nRapport de classification :\n" + classification_report(y_val, y_pred))


    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    logger.info(f"Modèle sauvegardé avec succès dans : {MODEL_PATH}")

if __name__ == "__main__":
    train_model()