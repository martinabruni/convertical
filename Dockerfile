# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

# Run Instructions:
# 1. Build the Docker image:
#    docker build -t xlsx-to-ics .
# 2. Run the container:
#    docker run -d -p 5000:5000 --name xlsx-to-ics-app xlsx-to-ics
# 3. Access the app in your browser at http://localhost:5000