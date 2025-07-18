#!/bin/bash
set -e

IMG_VERSION=$1
CLUSTER_NAME=$2

get_help() {
  echo "Usage: $0 [IMG_VERSION] [CLUSTER_NAME]"
  echo "  IMG_VERSION: Version of the Docker images to build and load (e.g., v0.1.1)"
  echo "  CLUSTER_NAME: Name of the kind cluster (default: quotes-cluster)"
  echo "Example: $0 v0.1.1 quotes-cluster"
}

if [[ -z "$IMG_VERSION" ]] && [[ -z "$CLUSTER_NAME" ]]; then
  get_help
  exit 1
fi

cd backend

# Build Docker images
echo "Building server Docker image..."
docker build -t quotes-api:"${IMG_VERSION}" -f dockerfile .

cd ../frontend

echo "Building client Docker image..."
docker build -t quotes-frontend:"${IMG_VERSION}" -f dockerfile .

# Load images into kind cluster
echo "Loading server image into kind cluster..."
kind load docker-image quotes-api:"${IMG_VERSION}" --name "${CLUSTER_NAME}"

echo "Loading client image into kind cluster..."
kind load docker-image quotes-frontend:"${IMG_VERSION}" --name "${CLUSTER_NAME}"

echo "Docker images built and loaded to ${CLUSTER_NAME} successfully!"
