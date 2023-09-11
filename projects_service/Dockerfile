# Dockerfile for Projects service
# Use an official Python runtime as a parent image
FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the current directory contents into the container at /api_gateway_service
COPY projects_service /code/projects_service
COPY common_components /code/common_components

# Run main.py when the container launches
CMD ["uvicorn", "projects_router:app", "--host", "0.0.0.0", "--port", "8002"]