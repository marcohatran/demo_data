# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install kafka-python streamlit

# Copy the application code
COPY . .

# Run the application
CMD ["streamlit", "run", "realtime_dashboard.py"]
