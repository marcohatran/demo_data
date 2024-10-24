import json
import random
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime,timezone

# Load customer and sales data from JSON files
with open('customers.json', 'r') as f:
    customer_profiles = json.load(f)

with open('sales.json', 'r') as f:
    sales_profiles = json.load(f)

# Simulate customer data enrichment from the JSON file
def enrich_customer(user_id):
    for profile in customer_profiles:
        if profile["user_id"] == user_id:
            return profile
    return {}

# Simulate sales assignment from loaded sales profiles
def assign_sales():
    return random.choice(sales_profiles)

# Create Kafka consumer and producer
consumer = KafkaConsumer(
    'poc_event_dropoff',
    bootstrap_servers=['10.100.21.136:9092', '10.100.21.137:9092', '10.100.21.139:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sales_assign_lead_new_new_group_2'
)

producer = KafkaProducer(
    bootstrap_servers=['10.100.21.136:9092', '10.100.21.137:9092', '10.100.21.139:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Process messages from Kafka topic
for message in consumer:
    event_data = json.loads(message.value.decode('utf-8'))
    print(f"Received event: {event_data}")

    # Check if the user dropped off from the product introduction
    if event_data['event'] == 'dropoff':
        user_id = event_data['user_id']
        
        # Enrich customer data based on user ID
        enriched_customer = enrich_customer(user_id)
        if not enriched_customer:
            print(f"No customer profile found for user ID {user_id}")
            continue

        # Assign a sales representative randomly from the sales profiles
        assigned_sales = assign_sales()

        # Create result payload with enriched customer and assigned sales info
        result_payload = {
            "customer_info": enriched_customer,
            "sales_info": assigned_sales,
            "product_name": event_data['product_name'],
            "event_timestamp": event_data['timestamp'],
            "processed_timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Send the result to the lead topic
        producer.send('poc_lead_create_topic', value=result_payload)
        print(f"Sent lead: {result_payload}")
