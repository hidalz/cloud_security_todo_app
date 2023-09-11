#!/bin/bash
# 2 - Run in root folder > ./devops/scripts/helm_install_microservices.sh

# List of service names
services=("api-gateway-service" "auth-service" "projects-service" "tasks-service" "users-service")

# Add nginx-ingress repo and install it
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx

# Loop through the services and install them using Helm
for service in "${services[@]}"
do
  echo "Uninstalling $service..."
  helm uninstall "$service"
  
  echo "Installing $service..."
  helm install "$service" ./devops/"$service"-chart
done

echo "All services have been installed."
