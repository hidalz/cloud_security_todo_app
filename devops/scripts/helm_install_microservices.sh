#!/bin/bash
# 2 - Run this script from devops directory using ./scripts/helm_install_microservices.sh
# List of service names
services=("api-gateway-service" "auth-service" "projects-service" "tasks-service" "users-service")

# Loop through the services and install them using Helm
for service in "${services[@]}"
do
  echo "Installing $service..."
  helm install "$service" ./"$service"-chart
done

echo "All services have been installed."
