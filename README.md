# File Upload Application with MinIO and AWS S3

This project is a **full-stack file upload application** where users can upload files via a React frontend. Files are first stored in a **local MinIO server** and then periodically synced to **AWS S3** using a Python backend with a cron-like scheduler.  

The application is fully **containerized using Docker** for easy setup and deployment.

---

## 🏗️ Project Structure

my-project/
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