import uuid
from datetime import datetime

readings = []

def save_reading(patient_id: str, data: dict):
    item = {
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "heart_rate": data["heart_rate"],
        "temperature": data["temperature"],
        "spo2": data["spo2"],
        "blood_pressure": data["blood_pressure"],
        "timestamp": datetime.utcnow().isoformat(),
    }
    readings.append(item)
    return item

def get_my_readings(patient_id: str):
    return [r for r in readings if r["patient_id"] == patient_id]

def get_all_readings():
    return readings