#Using official Python image from the Docker Hub
FROM python:3.10.12-slim

#Set working directory in container
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*
#Copy requirements.txt into the working directory and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire code to the container
COPY . .

#Expose the port the app runs on
EXPOSE 8000

#Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

