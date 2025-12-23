import logging
import sys
from pathlib import Path

# Import des fonctions de vos scripts
from download_data import download_dataset
from clean_transform import transform_all_data
from load_final import upload_files_to_s3

# Configuration du logging pour le suivi dans les logs GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def run_data_pipeline():
    """Orchestre les étapes du Data Pipeline : Ingestion, Nettoyage et Stockage S3."""
    logger.info("=== DÉMARRAGE DU DATA PIPELINE ETL ===")

    try:
        # Étape 1 : Téléchargement des données depuis Kaggle
        logger.info("Étape 1/3 : Téléchargement des données...")
        download_dataset()
        logger.info("Téléchargement terminé avec succès.")

        # Étape 2 : Nettoyage et transformation (Train & Test)
        logger.info("Étape 2/3 : Nettoyage et transformation des données...")
        transform_all_data()
        logger.info("Transformation terminée avec succès.")

        # Étape 3 : Chargement des fichiers finaux sur AWS S3
        logger.info("Étape 3/3 : Chargement vers AWS S3...")
        success = upload_files_to_s3()
        
        if success:
            logger.info("=== DATA PIPELINE TERMINÉ AVEC SUCCÈS ===")
        else:
            logger.error("Échec lors du chargement des fichiers sur S3.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Erreur critique durant le pipeline : {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_data_pipeline()