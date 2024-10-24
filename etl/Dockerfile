# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install psycopg2-binary kafka-python

# Copy the application code
COPY . .

CMD ["python", "app.py"]