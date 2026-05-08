from datetime import datetime
import uuid

alerts = []

def check_reading_rules(user_id: str, reading: dict):
    now = datetime.utcnow().isoformat()
    if reading["heart_rate"] > 140:
        alerts.append({
            "id": str(uuid.uuid4()),
            "type": "HEART_RATE",
            "message": "Abnormally high heart rate detected",
            "severity": "high",
            "user_id": user_id,
            "timestamp": now,
        })
    if reading["spo2"] < 90:
        alerts.append({
            "id": str(uuid.uuid4()),
            "type": "SPO2",
            "message": "Low oxygen saturation detected",
            "severity": "high",
            "user_id": user_id,
            "timestamp": now,
        })