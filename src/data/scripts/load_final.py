import boto3
import os
import logging
from pathlib import Path
from botocore.exceptions import NoCredentialsError, ClientError

# --- Configuration "à la main" ---
BUCKET_NAME = "s3g1gm04"
DATA_DIR = Path("src/data/datasets")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def upload_files_to_s3():
    # Récupération des secrets injectés par GitHub Actions
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_REGION')

    if not access_key or not secret_key:
        logging.error("Clés AWS introuvables dans l'environnement.")
        return False

    # Fichiers à envoyer vers S3
    files_to_upload = {
        "cleaned_train.csv": "data/cleaned_train.csv",
        "cleaned_test.csv": "data/cleaned_test.csv"
    }

    # Initialisation du client S3 avec les secrets
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    try:
        for local_name, s3_key in files_to_upload.items():
            local_path = DATA_DIR / local_name
            if local_path.exists():
                logging.info(f"Envoi de {local_name} vers s3://{BUCKET_NAME}/{s3_key}")
                s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
            else:
                logging.warning(f"Fichier local non trouvé : {local_path}")
        return True

    except ClientError as e:
        logging.error(f"Erreur AWS : {e}")
        return False

if __name__ == "__main__":
    upload_files_to_s3()