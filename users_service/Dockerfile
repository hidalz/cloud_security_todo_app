# Dockerfile for users_service
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container, same with common components & requirements
COPY users_service /app/users_service
COPY common_components /app/common_components
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8004 available to the world outside this container
EXPOSE 8004

# Define environment variable
ENV NAME users_service

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
