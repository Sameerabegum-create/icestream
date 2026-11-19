import pandas as pd
import json
from pathlib import Path
from kafka import KafkaProducer

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "output" / "processed" / "online_retail_prepared.csv"

TOPIC = "retail-events"
BATCH_SIZE = 1000

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value, default=str
    ).encode("utf-8")
)

print("Starting IceStream dataset producer...")

total_sent = 0

try:
    for chunk in pd.read_csv(INPUT_FILE, chunksize=BATCH_SIZE):
        for record in chunk.to_dict(orient="records"):
            cleaned_record = {
                key: None if pd.isna(value) else value
                for key, value in record.items()
            }
            producer.send(TOPIC, value=cleaned_record)

        producer.flush()
        total_sent += len(chunk)
        print(f"Total records sent: {total_sent}")

    print("Full dataset streaming completed!")

finally:
    producer.close()
