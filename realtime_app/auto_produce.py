from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime,timezone
import random
import json

producer = KafkaProducer(
    bootstrap_servers=['10.100.21.136:9092', '10.100.21.137:9092', '10.100.21.139:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open('first.json', 'r') as f:
    customer_profiles = json.load(f)


for customer in customer_profiles:
    product_list = ["Saving", "Credit", "Investment"]
    product = random.choice(product_list)
    payload = {
	"user_id": customer["user_id"],
	"product_name": product,
	"event": "dropoff",
	"timestamp": datetime.now(timezone.utc).isoformat()
    }
    producer.send('poc_event_dropoff', value=payload)
    print(payload)


