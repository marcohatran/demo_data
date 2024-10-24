# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install streamlit requests streamlit_autorefresh pandas

# Copy the application code
COPY . .

EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "realtime_dashboard.py"]
