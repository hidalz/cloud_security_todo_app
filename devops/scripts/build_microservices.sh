#!/bin/bash
# 1 - Run in root folder > ./devops/scripts/build_microservices.sh

# List of your microservices directories
microservices=("auth_service" "api_gateway_service" "users_service" "tasks_service" "projects_service")

# Iterate through the microservices and build each one
for service in "${microservices[@]}"; do
  echo "Building $service..."
  docker build -t "${service}" -f "${service}/Dockerfile" .
done

