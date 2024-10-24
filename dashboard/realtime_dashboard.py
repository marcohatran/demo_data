import streamlit as st
import pandas as pd
import requests
import time
from streamlit_autorefresh import st_autorefresh


# API base URL
API_BASE_URL = "http://ip:8000"



# Page configuration
st.set_page_config(page_title="Real-Time Sales Dashboard", layout="wide")

st.title("Real-Time Lead Assignment Dashboard")

# Metrics explanation
st.markdown("""
    This dashboard presents **real-time data**. The metrics below provide insights into the following:
    - **Total Leads Processed**: The total number of leads that have been processed.
    - **Top Sales Reps**: A bar chart displaying the number of leads assigned to each sales representative.
    - **Product Interest**: Shows the number of customers who showed interest in one of the three products: Saving, Credit, or Investment.
    - **Product Conversion Rate**: Shows the distribution of leads between the three products.
    - **Recent Leads**: This table shows the most recent customer leads, including the product they are interested in, their assigned sales representative, and other details.
""")

# Function to get metrics from the FastAPI
def fetch_metrics():
    response = requests.get(f"{API_BASE_URL}/metrics")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get recent leads from the FastAPI
def fetch_recent_leads():
    response = requests.get(f"{API_BASE_URL}/leads")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Refresh every 30 seconds
def display_dashboard():
    with st.spinner('Loading data...'):
        # Fetch metrics data from the API
        metrics = fetch_metrics()
        if metrics:
            st.subheader("Total Leads Processed")
            st.write(metrics['total_leads'])

            col1, col2 = st.columns(2)

            # with col1:
            #     st.subheader("Top Sales Reps")
            #     # Format top sales reps data
            #     sales_reps_data = pd.DataFrame(metrics['top_sales_reps'])
            #     sales_reps_data.columns = ['Sales Rep', 'Leads Processed']
            #     # Display bar chart
            #     st.bar_chart(sales_reps_data.set_index('Sales Rep'))
            with col1:
                st.subheader("Top Sales Reps")
                
                # Format top sales reps data
                sales_reps_data = pd.DataFrame(metrics['top_sales_reps'])
                if not sales_reps_data.empty:
                    sales_reps_data.columns = ['Sales Rep', 'Leads Processed']
                    # Display bar chart
                    st.bar_chart(sales_reps_data.set_index('Sales Rep'))
                else:
                    st.write("No sales data available.")

            with col2:
                st.subheader("Product Interest")
                # Format product interest data
                product_interest_data = pd.DataFrame(metrics['product_interest'])
                product_interest_data.columns = ['Product', 'Customer Interest']
                # Display bar chart
                st.bar_chart(product_interest_data.set_index('Product'))

            # Fetch and display recent leads
            st.subheader("Recent Leads")
            leads = fetch_recent_leads()
            if leads:
                lead_df = pd.DataFrame(leads)
                st.dataframe(lead_df)

# Refresh the page every 30 seconds
# st_autorefresh(interval=30 * 1000)  # interval in milliseconds
st_autorefresh(interval=30 * 1000)
print("refresh")
# Display the dashboard for the first time
display_dashboard()
