from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from datetime import timedelta
from io import BytesIO  # 👈 import this
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

app = FastAPI()

# === Environment variables ===
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "uploads")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

AWS_BUCKET = os.getenv("AWS_BUCKET", "minio-s3-bucket-v1")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL like ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect to local MinIO (port 9000)
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)


BUCKET_NAME = "uploads"

if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read the file data
    file_data = await file.read()
    file_stream = BytesIO(file_data)  # 👈 wrap bytes in a stream

    # Upload to MinIO
    minio_client.put_object(
        MINIO_BUCKET,
        file.filename,
        file_stream,
        length=len(file_data),
        content_type=file.content_type
    )

    # Generate temporary URL (valid for 1 hour)
    url = minio_client.presigned_get_object(
        MINIO_BUCKET, file.filename, expires=timedelta(hours=1)
    )

    return {"minio_url": url, "filename": file.filename}


@app.get("/files")
async def list_files():
    files = []

    for obj in minio_client.list_objects(MINIO_BUCKET, recursive=True):
        try:
            url = minio_client.presigned_get_object(
                MINIO_BUCKET,
                obj.object_name,
                expires=timedelta(hours=1),
                response_headers={
                    "response-content-disposition": "inline"
                }
            )
            files.append({"name": obj.object_name, "source": "MinIO", "url": url})
        except Exception as e:
            print(f"Error generating presigned URL: {e}")


    # S3 files
    s3_objects = s3_client.list_objects_v2(Bucket=AWS_BUCKET).get('Contents', [])
    for obj in s3_objects:
        url = f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{obj['Key']}"
        files.append({"name": obj['Key'], "source": "S3", "url": url})

    return JSONResponse(content={"files": files})
