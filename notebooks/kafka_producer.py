import pandas as pd
import json
from pathlib import Path
from kafka import KafkaProducer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "output" / "processed" / "online_retail_prepared.csv"

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value, default=str
    ).encode("utf-8")
)

TOPIC = "retail-events"

# Read prepared dataset
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded:", len(df), "records")

# Send records to Kafka
try:
    for index, row in df.iterrows():
        record = row.astype(object).where(pd.notna(row), None).to_dict()
        producer.send(TOPIC, value=record)

        if (index + 1) % 1000 == 0:
            producer.flush()
            print(f"Sent {index + 1} records")

    producer.flush()
    print("All records sent successfully!")

finally:
    producer.close()
