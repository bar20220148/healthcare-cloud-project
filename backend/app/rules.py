from .db import save_alert

def check_reading_rules(user_id: str, reading: dict):
    created = []

    if reading["heart_rate"] > 140:
        created.append(
            save_alert(
                user_id=user_id,
                alert_type="HEART_RATE",
                message="Abnormally high heart rate detected",
                severity="high",
            )
        )

    if reading["spo2"] < 90:
        created.append(
            save_alert(
                user_id=user_id,
                alert_type="SPO2",
                message="Low oxygen saturation detected",
                severity="high",
            )
        )

    return created

def add_security_alert(user_id: str, message: str):
    return save_alert(
        user_id=user_id,
        alert_type="SECURITY",
        message=message,
        severity="medium",
    )