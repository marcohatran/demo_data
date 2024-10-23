import streamlit as st
import json
import pandas as pd
from kafka import KafkaConsumer

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'poc_create_lead_topic',
    bootstrap_servers=[],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='streamlit_dashboard_group_123',
    consumer_timeout_ms=1000  # Timeout after 1 second if no messages
)

# Initialize session state for metrics and processed leads
if 'lead_data' not in st.session_state:
    st.session_state.lead_data = []
if 'sales_count' not in st.session_state:
    st.session_state.sales_count = {}
if 'product_interest' not in st.session_state:
    st.session_state.product_interest = {"Saving": 0, "Credit": 0, "Investment": 0}
if 'processed_leads' not in st.session_state:
    st.session_state.processed_leads = set()  # Set to track processed lead identifiers

# Streamlit page configuration
st.set_page_config(page_title="Real-Time Sales Dashboard", layout="wide")

# Title
st.title("Real-Time Lead Assignment Dashboard")

# Metrics explanations
st.markdown("""
    This dashboard presents **real-time data** . The metrics below provide insights into the following:
    - **Total Leads Processed**: The total number of leads that have been processed.
    - **Top Sales Reps**: A bar chart displaying the number of leads assigned to each sales representative.
    - **Product Interest**: Shows the number of customers who showed interest in one of the three products: Saving, Credit, or Investment.
    - **Product Conversion Rate**: Shows the distribution of leads between the three products.
    """)

# Create columns for metrics
col1, col2, col3 = st.columns(3)

# Function to update metrics
def update_metrics(lead):
    customer_info = lead['customer_info']
    sales_info = lead['sales_info']
    product_name = lead['product_name']
    sales_name = sales_info['sales_name']
    lead_id = customer_info["name"]  # Assuming customer name is unique for this demo

    # Check if the lead has already been processed
    if lead_id in st.session_state.processed_leads:
        return  # Skip already processed leads

    # Update sales count
    if sales_name not in st.session_state.sales_count:
        st.session_state.sales_count[sales_name] = 0
    st.session_state.sales_count[sales_name] += 1

    # Update product interest count (only for Saving, Credit, and Investment)
    if product_name in st.session_state.product_interest:
        st.session_state.product_interest[product_name] += 1

    # Store lead data for display
    st.session_state.lead_data.append({
        "Customer Name": customer_info["name"],
        "Product Name": product_name,
        "Sales Rep": sales_name,
        "Balance": customer_info["balance"],
        "Score": customer_info["score"]
    })

    # Mark this lead as processed
    st.session_state.processed_leads.add(lead_id)

# Function to render dashboard components
def render_dashboard():
    # Real-time data update in Streamlit
    with col1:
        st.subheader("Total Leads Processed")
        st.write(f"{len(st.session_state.lead_data)} leads have been processed in real time.")
        st.markdown("*This shows the total number of customers who have shown interest in a product and were assigned to a sales representative.*")

        st.subheader("Top Sales Reps")
        if st.session_state.sales_count:
            st.bar_chart(pd.DataFrame.from_dict(st.session_state.sales_count, orient='index', columns=['Sales Count']))
        else:
            st.write("No data yet.")

        st.markdown("*This chart shows how many leads have been assigned to each sales representative.*")

    with col2:
        st.subheader("Product Interest")
        if st.session_state.product_interest:
            st.bar_chart(pd.DataFrame.from_dict(st.session_state.product_interest, orient='index', columns=['Interest']))
        else:
            st.write("No data yet.")

        st.markdown("*This chart shows which of the three products (Saving, Credit, Investment) customers have shown the most interest in.*")

    with col3:
        st.subheader("Product-wise Conversion Rate")
        total_leads = sum(st.session_state.product_interest.values())
        if total_leads > 0:
            conversion_rate_df = pd.DataFrame.from_dict(st.session_state.product_interest, orient='index', columns=['Leads'])
            conversion_rate_df['Percentage'] = (conversion_rate_df['Leads'] / total_leads) * 100
            st.bar_chart(conversion_rate_df['Percentage'])
        else:
            st.write("No data yet.")
        st.markdown("*This chart shows the percentage of leads for each product (Saving, Credit, and Investment). It helps visualize the conversion rate between the products.*")

    st.subheader("Recent Leads")
    if st.session_state.lead_data:
        st.dataframe(pd.DataFrame(st.session_state.lead_data))
    else:
        st.write("No recent leads to show yet.")
    st.markdown("*This table shows the most recent customer leads, including the product they are interested in, their assigned sales representative, and other details.*")

# Main loop to consume Kafka messages and update dashboard
def consume_and_update():
    # Process messages from the Kafka consumer with a timeout
    messages = consumer.poll(timeout_ms=1000)  # Poll for 1 second
    if messages:
        for _, message_batch in messages.items():
            for message in message_batch:
                lead = json.loads(message.value.decode('utf-8'))
                update_metrics(lead)

    # Render the dashboard after processing any messages
    render_dashboard()

# Streamlit's main execution loop
if __name__ == "__main__":
    # Call function to consume messages and update the dashboard
    consume_and_update()
