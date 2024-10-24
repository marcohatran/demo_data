import json
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to generate a fake customer profile
def generate_customer(user_id):
    return {
        "user_id": str(user_id),
        "name": fake.name(),
        "phone": fake.phone_number(),
        "score": random.randint(1, 100),  # Credit score range
        "location": fake.city(),
        "gender": random.choice(["male", "female"]),
        "balance": round(random.uniform(500.0, 50000.0), 2),  # Random balance
        "casa_last_3_months": random.randint(1000, 30000),
        "birthdate": fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50).isoformat()
    }

# Function to generate a fake sales profile
def generate_sales(sales_id):
    return {
        "sales_id": str(sales_id),
        "sales_name": fake.name(),
    }

# Generate 200 fake customers
customers = [generate_customer(user_id) for user_id in range(100001, 100201)]

# Generate 20 fake sales profiles
sales = [generate_sales(sales_id) for sales_id in range(1, 21)]

# Write customers to JSON file
with open('customers.json', 'w') as customer_file:
    json.dump(customers, customer_file, indent=4)

# Write sales to JSON file
with open('sales.json', 'w') as sales_file:
    json.dump(sales, sales_file, indent=4)

print("Fake customer and sales data generated!")
