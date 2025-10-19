import boto3
from minio import Minio
from datetime import datetime
import os
import mimetypes
from dotenv import load_dotenv

load_dotenv()

# === Environment variables ===
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "uploads")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

AWS_BUCKET = os.getenv("AWS_BUCKET", "minio-s3-bucket-v1")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")


# === Clients ===
# Local MinIO
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


# === Sync Function ===
def sync_minio_to_s3():
    print(f"Starting sync job at {datetime.now()}...")

    objects = minio_client.list_objects(MINIO_BUCKET, recursive=True)

    for obj in objects:
        obj_name = obj.object_name
        print(f"Processing: {obj_name}")

        try:
            # Get the file from MinIO
            data = minio_client.get_object(MINIO_BUCKET, obj_name)

            # Guess the content type from the filename
            content_type, _ = mimetypes.guess_type(obj_name)
            content_type = content_type or 'application/octet-stream'

            # Upload to AWS S3 with metadata
            s3_client.upload_fileobj(
                Fileobj=data,
                Bucket=AWS_BUCKET,
                Key=obj_name,
                ExtraArgs={
                    'ContentType': content_type,
                    'ContentDisposition': 'inline'
                }
            )

            print(f"✅ Uploaded {obj_name} with Content-Type: {content_type}")

            # Delete the object from MinIO after successful upload
            minio_client.remove_object(MINIO_BUCKET, obj_name)
            print(f"🗑️  Deleted {obj_name} from MinIO.")

        except Exception as e:
            print(f"❌ Error syncing {obj_name}: {e}")

        finally:
            try:
                data.close()
                data.release_conn()
            except:
                pass

    print("🎉 Sync completed!")


# === Entry Point ===
if __name__ == "__main__":
    sync_minio_to_s3()
