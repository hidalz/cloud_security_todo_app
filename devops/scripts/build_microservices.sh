#!/bin/bash
# 1 - Run in root folder > ./devops/scripts/build_microservices.sh

# List of your microservices directories
microservices=("auth_service" "api_gateway_service" "users_service" "tasks_service" "projects_service")

# Use Minikube Docker environment
eval $(minikube -p minikube docker-env)

# Iterate through the microservices and build and push each one
for service in "${microservices[@]}"; do
  echo "Building and pushing $service..."
  # Build the image using localhost:49495 registry
  docker build -t "${service}" -f "${service}/Dockerfile" .
  
  # Push the image to the Docker daemon on localhost
  docker push "localhost:5000/${service}:latest"
done

