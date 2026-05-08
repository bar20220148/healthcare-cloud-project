from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class ReadingIn(BaseModel):
    heart_rate: int
    temperature: float
    spo2: int
    blood_pressure: str