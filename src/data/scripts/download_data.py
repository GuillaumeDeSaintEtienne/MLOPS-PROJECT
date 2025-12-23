import kagglehub
import shutil
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
DATASET_NAME = "parisrohan/credit-score-classification"
DESTINATION_PATH = Path("src/data/datasets") 

def download_dataset():
    """Télécharge le dataset depuis Kaggle et déplace les CSV vers le dossier local."""
    
    # 1. Téléchargement via Kagglehub
    logger.info(f"Téléchargement du dataset {DATASET_NAME} depuis Kaggle...")
    try:
        cache_path = kagglehub.dataset_download(DATASET_NAME)
        logger.info(f"Dataset téléchargé dans le cache : {cache_path}")
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement Kaggle : {e}")
        raise

    # 2. Création du dossier cible si nécessaire
    logger.info(f"Vérification du dossier de destination : {DESTINATION_PATH}")
    DESTINATION_PATH.mkdir(parents=True, exist_ok=True)

    # 3. Déplacement des fichiers CSV
    logger.info("Déplacement des fichiers CSV...")
    files_moved = 0

    for file_name in os.listdir(cache_path):
        if file_name.endswith(".csv"):
            source = Path(cache_path) / file_name
            dest = DESTINATION_PATH / file_name
            
            if dest.exists():
                logger.info(f"Le fichier {file_name} existe déjà dans {DESTINATION_PATH}. Passage.")
            else:
                shutil.move(str(source), str(dest))
                logger.info(f"Déplacé : {file_name}")
                files_moved += 1

    if files_moved == 0:
        logger.info("Aucun nouveau fichier CSV n'a été déplacé.")
    else:
        logger.info(f"Succès : {files_moved} fichiers ont été installés dans {DESTINATION_PATH}.")

if __name__ == "__main__":
    download_dataset()