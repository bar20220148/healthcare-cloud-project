from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging

from .models import LoginRequest, ReadingIn
from .auth import login_user, get_current_user
from .db import (
    save_reading,
    get_my_readings,
    get_all_readings,
    get_all_alerts,
    export_readings_to_s3,
)
from .rules import check_reading_rules, add_security_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("healthcare-api")

app = FastAPI(title="Healthcare Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}

@app.post("/auth/login")
def login(data: LoginRequest):
    return login_user(data.username, data.password)

@app.post("/readings")
def create_reading(data: ReadingIn, user=Depends(get_current_user)):
    if user["role"] != "patient":
        add_security_alert(user["sub"], "Non-patient tried to submit patient reading")
        raise HTTPException(status_code=403, detail="Only patients can submit readings")

    item = save_reading(user["sub"], data.model_dump())
    created_alerts = check_reading_rules(user["sub"], item)
    logger.info("Reading submitted by %s", user["username"])
    return {"reading": item, "alerts_created": created_alerts}

@app.get("/readings/me")
def my_readings(user=Depends(get_current_user)):
    return get_my_readings(user["sub"])

@app.get("/readings/all")
def all_readings(user=Depends(get_current_user)):
    if user["role"] != "doctor":
        add_security_alert(user["sub"], "Patient tried to access doctor route")
        raise HTTPException(status_code=403, detail="Doctor only")
    return get_all_readings()

@app.get("/alerts")
def alerts(user=Depends(get_current_user)):
    if user["role"] != "doctor":
        add_security_alert(user["sub"], "Patient tried to access doctor alerts")
        raise HTTPException(status_code=403, detail="Doctor only")
    return get_all_alerts()

@app.post("/exports/me")
def export_my_readings(user=Depends(get_current_user)):
    if user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can export their readings")
    exported = export_readings_to_s3(user["sub"])
    logger.info("Export created for %s", user["username"])
    return exported