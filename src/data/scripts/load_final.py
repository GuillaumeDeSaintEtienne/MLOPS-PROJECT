import boto3
import os
import logging
from pathlib import Path
from botocore.exceptions import ClientError

# --- Configuration des chemins locaux ---
DATA_DIR = Path("src/data/datasets")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def upload_files_to_s3():
    """Charge les fichiers nettoyés vers S3 en utilisant les secrets d'environnement."""
    
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_REGION')
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    if not all([access_key, secret_key, bucket_name]):
        logger.error("Erreur : Secrets AWS (ID, Key ou Bucket Name) introuvables.")
        return False

    files_to_upload = {
        "cleaned_train.csv": "data/cleaned_train.csv",
        "cleaned_test.csv": "data/cleaned_test.csv"
    }

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    success = True
    try:
        for local_name, s3_key in files_to_upload.items():
            local_path = DATA_DIR / local_name
            
            if local_path.exists():
                logger.info(f"Envoi de {local_name} vers s3://{bucket_name}/{s3_key}")
                s3.upload_file(str(local_path), bucket_name, s3_key)
            else:
                logger.warning(f"Fichier local non trouvé : {local_path}")
                success = False
                
        return success

    except ClientError as e:
        logger.error(f"Erreur lors du transfert AWS : {e}")
        return False

if __name__ == "__main__":
    upload_files_to_s3()