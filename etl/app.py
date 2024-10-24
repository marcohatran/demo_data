from kafka import KafkaConsumer
import psycopg2
import json

# Kafka consumer configuration
consumer = KafkaConsumer(
    'lead_topic_poc',
    bootstrap_servers=[],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='lead_consumer_group'
)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="10.100.21.135",
    database="poc_stream",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Function to insert lead data into PostgreSQL
def insert_lead_data(lead_data):
    sql = """
        INSERT INTO insights.leads (
            user_id, customer_name, customer_phone, customer_score, customer_location, customer_gender, 
            customer_balance, customer_casa_last_3_months, customer_birthdate, product_name, 
            sales_rep_id, sales_rep_name, event_timestamp, processed_timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    customer_info = lead_data['customer_info']
    sales_info = lead_data['sales_info']
    values = (
        customer_info['user_id'],
        customer_info['name'],
        customer_info['phone'],
        customer_info['score'],
        customer_info['location'],
        customer_info['gender'],
        customer_info['balance'],
        customer_info['casa_last_3_months'],
        customer_info['birthdate'],
        lead_data['product_name'],
        sales_info['sales_id'],
        sales_info['sales_name'],
        lead_data['event_timestamp'],
        lead_data['processed_timestamp']
    )
    cur.execute(sql, values)
    conn.commit()

# Kafka consumer loop
for message in consumer:
    lead = json.loads(message.value.decode('utf-8'))
    insert_lead_data(lead)

# Close connection
cur.close()
conn.close()
