from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import LoginRequest, ReadingIn
from .auth import login_user, get_current_user
from .db import save_reading, get_my_readings, get_all_readings
from .rules import check_reading_rules, alerts

app = FastAPI(title="Healthcare Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/login")
def login(data: LoginRequest):
    return login_user(data.username, data.password)

@app.post("/readings")
def create_reading(data: ReadingIn, user=Depends(get_current_user)):
    if user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can submit readings")
    item = save_reading(user["sub"], data.model_dump())
    check_reading_rules(user["sub"], item)
    return item

@app.get("/readings/me")
def my_readings(user=Depends(get_current_user)):
    return get_my_readings(user["sub"])

@app.get("/readings/all")
def all_readings(user=Depends(get_current_user)):
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    return get_all_readings()

@app.get("/alerts")
def get_alerts(user=Depends(get_current_user)):
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    return alerts