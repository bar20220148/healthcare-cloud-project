import os
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
READINGS_TABLE = os.getenv("READINGS_TABLE", "Readings")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
readings_table = dynamodb.Table(READINGS_TABLE)

def save_reading(patient_id: str, data: dict):
    item = {
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": data["heart_rate"],
        "temperature": data["temperature"],
        "spo2": data["spo2"],
        "blood_pressure": data["blood_pressure"],
    }
    readings_table.put_item(Item=item)
    return item

def get_my_readings(patient_id: str):
    response = readings_table.query(
        KeyConditionExpression=Key("patient_id").eq(patient_id)
    )
    return response.get("Items", [])

def get_all_readings():
    response = readings_table.scan()
    return response.get("Items", [])