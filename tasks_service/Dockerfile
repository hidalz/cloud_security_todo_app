# Dockerfile for tasks service
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container, same with common components & requirements
COPY tasks_service /app/tasks_service
COPY common_components /app/common_components
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8003 available to the world outside this container
EXPOSE 8003

# Define environment variable
ENV NAME tasks_service

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
