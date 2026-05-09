import os
import json
from datetime import datetime
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
READINGS_TABLE = os.getenv("READINGS_TABLE", "Readings")
ALERTS_TABLE = os.getenv("ALERTS_TABLE", "Alerts")
S3_BUCKET = os.getenv("S3_BUCKET", "healthcare-project-exports")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)

readings_table = dynamodb.Table(READINGS_TABLE)
alerts_table = dynamodb.Table(ALERTS_TABLE)

def normalize_value(value):
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: normalize_value(v) for k, v in value.items()}
    return value

def save_reading(patient_id: str, data: dict):
    item = {
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": int(data["heart_rate"]),
        "temperature": Decimal(str(data["temperature"])),
        "spo2": int(data["spo2"]),
        "blood_pressure": data["blood_pressure"],
    }
    readings_table.put_item(Item=item)
    return normalize_value(item)

def get_my_readings(patient_id: str):
    response = readings_table.query(
        KeyConditionExpression=Key("patient_id").eq(patient_id)
    )
    return normalize_value(response.get("Items", []))

def get_all_readings():
    response = readings_table.scan()
    return normalize_value(response.get("Items", []))

def save_alert(user_id: str, alert_type: str, message: str, severity: str):
    item = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "type": alert_type,
        "message": message,
        "severity": severity,
    }
    alerts_table.put_item(Item=item)
    return normalize_value(item)

def get_alerts_for_user(user_id: str):
    response = alerts_table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
    )
    return normalize_value(response.get("Items", []))

def get_all_alerts():
    response = alerts_table.scan()
    return normalize_value(response.get("Items", []))

def export_readings_to_s3(patient_id: str):
    readings = get_my_readings(patient_id)
    key = f"exports/{patient_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
    body = json.dumps(readings, indent=2)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/json"
    )
    return {
        "bucket": S3_BUCKET,
        "key": key
    }