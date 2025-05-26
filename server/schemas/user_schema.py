from pydantic import BaseModel, EmailStr, Field, validator
from typing import Literal

class UserRegister(BaseModel):
    nama: str
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @validator("password")
    def password_min_length(cls, value):
        if len(value) < 8:
            raise ValueError("Password harus memiliki minimal 8 karakter")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    usia: int
    berat_badan: float
    tinggi_badan: float
    jenis_kelamin: Literal["laki-laki", "perempuan"]
    aktivitas_fisik: Literal["sedentari","ringan", "sedang", "berat"]

class UserResponse(BaseModel):
    id: int
    nama: str  # Sesuaikan dengan nama kolom di database
    email: str  # Sesuaikan dengan kolom yang ada
    kalori: float
    bmr: float
    bmi: float
    klasifikasi: str

    class Config:
        orm_mode = True

class UserResponseUsernameEmail(BaseModel):
    nama: str
    email: EmailStr

    class Config: 
        orm_mode = True

class UpdateBBTB(BaseModel):
    berat_badan: float
    tinggi_badan: float