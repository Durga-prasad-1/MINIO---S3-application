# File Upload Application with MinIO and AWS S3

This project is a **full-stack file upload application** where users can upload files via a React frontend. Files are first stored in a **local MinIO server** and then periodically synced to **AWS S3** using a Python backend with a cron-like scheduler.  

The application is fully **containerized using Docker** for easy setup and deployment.

---

## 🏗️ Project Structure
```
MINIO---S3-application/
├── backend/ # Python backend (FastAPI)
│ ├── backend.py # API for file upload and retrieval
│ ├── sync_minio_to_s3.py # Script to sync MinIO files to AWS S3
│ ├── requirements.txt # Python dependencies
│ ├── .env # Environment variables
│ └── pycache/
│
├── frontend/ # React frontend
│ ├── src/
│ ├── public/
│ ├── package.json
│ ├── .env
│ └── vite.config.js
│
├── docker-compose.yml # Docker orchestration
└── README.md
```
---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend  | React + Vite + Nginx |
| Backend   | FastAPI + Python 3.11 |
| Local Storage | MinIO (S3-compatible) |
| Cloud Storage | AWS S3 |
| Containerization | Docker & Docker Compose |

---

## ⚡ Features

- Upload files from the frontend to **local MinIO storage**
- Backend generates a temporary URL for the uploaded file
- **Periodic sync** of all MinIO files to AWS S3 (every 24 hours)
- Display files from both MinIO and S3 in the frontend
  - Image files show a **preview**
  - Non-image files are displayed as **downloadable links**
- Fully containerized for easy deployment

---

## ⚙️ Environment Variables

### Backend `.env`

```bash
# MinIO configuration
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=uploads

# AWS S3 configuration
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_BUCKET=YOUR_S3_BUCKET_NAME
AWS_REGION=YOUR_S3_REGION
```

---

## 🚀 Running the Application

Make sure Docker and Docker Compose are installed

Make sure that the minio server is running no the server laptop **important**

Cmd:
```cmd
.\minio.exe server <path_of_your_miniodata_folder> --console-address ":9001"
```
Example:
.\minio.exe server C:\minio_data --console-address ":9001"

Clone this repository and navigate to the project folder

Run:

```bash
docker-compose up --build
```

---

## Access the services

| Service  | URL                 |
|----------|---------------------|
| Frontend | http://localhost:3000 |

---

to manually word on cron job
```bash
docker exec -it sync-cron python /app/sync_minio_to_s3.py
```

---

## ⚠️ Common Issues

Backend cannot connect to MinIO
Make sure MINIO_ENDPOINT points to the Docker service name:

```
MINIO_ENDPOINT=minio:9000
```

MinIO default credentials warning
OK for development; use strong credentials for production

---

## Stopping the Application

```bash
docker-compose down
docker-compose down -v  # Remove volumes
```
