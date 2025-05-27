import numpy as np
import joblib
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.makanan import Makanan
from app.schemas.makanan_schema import MakananCreate, MakananResponse
from app.auth.auth_bearer import JWTBearer

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
MODEL_PATH = os.path.join(BASE_DIR, "..", "ML", "model_clustering_makanan.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "ML", "scaler_makanan.pkl")

router = APIRouter(
    prefix="/makanan",
    tags=["Makanan"],
    dependencies=[Depends(JWTBearer())]
)

def kategori_kalori(kal):
    if kal > 500:
        return "Tinggi"
    elif 200 <= kal <= 500:
        return "Sedang"
    else:
        return "Rendah"

kmeans = joblib.load('https://kipakxetfqnpinxeialy.supabase.co/storage/v1/object/sign/obsicare/model_clustering_makanan.pkl?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InN0b3JhZ2UtdXJsLXNpZ25pbmcta2V5X2QzNzBjMzA4LTI5ZDUtNGFmYS1hMTFmLTM2NTFiMjdmZTU0ZSJ9.eyJ1cmwiOiJvYnNpY2FyZS9tb2RlbF9jbHVzdGVyaW5nX21ha2FuYW4ucGtsIiwiaWF0IjoxNzQ4MzM3Mzc1LCJleHAiOjE3Nzk4NzMzNzV9.Yy9BbUF6AxNFZw3i9LgdF3ZrLrWLgmztTpL0BayGfC8')
scaler = joblib.load('https://kipakxetfqnpinxeialy.supabase.co/storage/v1/object/sign/obsicare/scaler_makanan.pkl?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InN0b3JhZ2UtdXJsLXNpZ25pbmcta2V5X2QzNzBjMzA4LTI5ZDUtNGFmYS1hMTFmLTM2NTFiMjdmZTU0ZSJ9.eyJ1cmwiOiJvYnNpY2FyZS9zY2FsZXJfbWFrYW5hbi5wa2wiLCJpYXQiOjE3NDgzMzc0NjYsImV4cCI6MTc3OTg3MzQ2Nn0.AbHmz3Z0hdcAHD_BPL1laqI1YFaBuUpGmvtjgaqkV40')

@router.post("/tambah_data_makanan", status_code=201)
def tambah_makanan(data: MakananCreate, db: Session = Depends(get_db)):
    kategori = kategori_kalori(data.kalori)
    fitur = np.array([[data.kalori, data.protein]])
    fitur_scaled = scaler.transform(fitur)
    cluster = int(kmeans.predict(fitur_scaled)[0])
    makanan = Makanan(nama=data.nama, kalori=data.kalori, protein=data.protein, kategori=kategori, cluster=cluster)
    db.add(makanan)
    db.commit()
    db.refresh(makanan)
    return makanan

@router.get("/")
def get_all_makanan(db: Session = Depends(get_db)):
    return db.query(Makanan).all()

@router.get("/search", response_model=list[MakananResponse])
def search_makanan(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return db.query(Makanan).filter(Makanan.nama.ilike(f"%{q}%")).all()

@router.get("/makanan/{makanan_id}", response_model=MakananResponse)
def get_detail_makanan(makanan_id: int, db: Session = Depends(get_db)):
    makanan = db.query(Makanan).filter(Makanan.id == makanan_id).first()
    if not makanan:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")
    return makanan

