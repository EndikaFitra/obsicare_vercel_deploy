from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from app.database import Base, engine
from app.routers import user, makanan, rekomendasi, auth  # ✅ auth dari routers

app = FastAPI(
    title="Obsicare API",
    description="API untuk Monitoring dan Rekomendasi Pola Makan Penderita Obesitas",
    version="1.0.0"
)

MODEL_URL = "https://kipakxetfqnpinxeialy.supabase.co/storage/v1/object/sign/obsicare/model_clustering_makanan.pkl?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InN0b3JhZ2UtdXJsLXNpZ25pbmcta2V5X2QzNzBjMzA4LTI5ZDUtNGFmYS1hMTFmLTM2NTFiMjdmZTU0ZSJ9.eyJ1cmwiOiJvYnNpY2FyZS9tb2RlbF9jbHVzdGVyaW5nX21ha2FuYW4ucGtsIiwiaWF0IjoxNzQ4MzM3NDI2LCJleHAiOjE3Nzk4NzM0MjZ9.L2HCoRpK2W8VtDvKNZ3mKUldrisyUbovKjOylYLz-Ks"
SCALER_URL = "https://kipakxetfqnpinxeialy.supabase.co/storage/v1/object/sign/obsicare/scaler_makanan.pkl?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InN0b3JhZ2UtdXJsLXNpZ25pbmcta2V5X2QzNzBjMzA4LTI5ZDUtNGFmYS1hMTFmLTM2NTFiMjdmZTU0ZSJ9.eyJ1cmwiOiJvYnNpY2FyZS9zY2FsZXJfbWFrYW5hbi5wa2wiLCJpYXQiOjE3NDgzMzc0NjYsImV4cCI6MTc3OTg3MzQ2Nn0.AbHmz3Z0hdcAHD_BPL1laqI1YFaBuUpGmvtjgaqkV40"
MODEL_PATH = "EndikaFitra/obsicare_vercel_deploy/server/ML/model_clustering_makanan.pkl"
SCALER_PATH = 'EndikaFitra/obsicare_vercel_deploy/server/ML/scaler_makanan.pkl'

def download_model():
    if not os.path.exists(MODEL_PATH):
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)

download_model()

Base.metadata.create_all(bind=engine)

origins = ["http://localhost", "http://localhost:6000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])  # ✅ Perbaiki ini
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(makanan.router, prefix="/makanan", tags=["Makanan"])
app.include_router(rekomendasi.router, prefix="/rekomendasi", tags=["Rekomendasi Makanan"])
