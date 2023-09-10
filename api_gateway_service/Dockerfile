# Dockerfile for API Gateway Service
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /api_gateway_service
WORKDIR /app

# Copy the current directory contents into the container at /api_gateway_service
COPY api_gateway_service /app/api_gateway_service
COPY common_components /app/common_components
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME api_gateway_service

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]