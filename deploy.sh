#!/bin/bash
set -e

ACTUAL_IMG_VERSION=$2
IMG_VERSION=$3
CLUSTER_NAME=quotes-cluster

get_help() {
  echo "Usage: $0 [manifests|helm] [ACTUAL_IMG_VERSION] [IMG_VERSION]"
  echo "  manifests: Apply Kubernetes manifests directly"
  echo "  helm: Apply Helm charts"
  echo "  ACTUAL_IMG_VERSION: Actual version of the Docker images to build and load (e.g., v0.1.0), check manifests and helm charts for the correct version"
  echo "  IMG_VERSION: Version of the Docker images to build and load (e.g., v0.1.1), this is the version that will be used in the manifests and helm charts"
  echo "Example: $0 manifests v0.1.0 v0.1.1"
}

kwait() {
  # Wait for a specific condition on a Kubernetes resource
  local resource=$1
  echo "Waiting for ${resource} to be ready..."
  kubectl wait -n quotes-app --for=condition=ready pod -l app=quotes,tier="${resource}" --timeout=120s
}

apply_manifests() {
  # Apply Kubernetes resources
  echo "Applying Kubernetes resources..."

  kubectl apply -f k8s/namespace.yaml
  kubectl apply -f k8s/db/secret.yaml
  kubectl apply -f k8s/db/service.yaml
  kubectl apply -f k8s/db/statefulset.yaml

  kwait "mysql"

  kubectl apply -f k8s/backend/configmap.yaml
  kubectl apply -f k8s/backend/deployment.yaml
  kubectl apply -f k8s/backend/service.yaml
  kubectl apply -f k8s/backend/ingress.yaml

  kwait "api"

  kubectl apply -f k8s/frontend/configmap.yaml
  kubectl apply -f k8s/frontend/deployment.yaml
  kubectl apply -f k8s/frontend/service.yaml
  kubectl apply -f k8s/frontend/ingress.yaml

  kwait "frontend"
}

apply_helm_charts() {
  # Apply Kubernetes resources
  echo "Applying Kubernetes resources..."

  helm upgrade --install db ./k8s/helm/db --namespace=quotes-app --create-namespace

  kwait "mysql"

  helm upgrade --install backend ./k8s/helm/backend --namespace=quotes-app

  kwait "api"

  helm upgrade --install frontend ./k8s/helm/frontend --namespace=quotes-app

  kwait "frontend"
}

# Main script execution starts here
if [ $# -lt 3 ] || [ $# -gt 3 ]; then
  get_help
  exit 1
fi

# Create multi-node Kind cluster
echo "Creating Kind cluster..."
# First, create a KIND cluster if it doesn't exist
if ! kind get clusters | grep -q "${CLUSTER_NAME}"; then
  echo "Creating kind cluster..."
  # Create cluster with special config for ingress
  kind create cluster --config k8s/cluster/kind-cluster-config.yaml
else
  echo "Kind cluster ${CLUSTER_NAME} already exists"
fi

# Install NGINX Ingress Controller
echo "Installing NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "Waiting for NGINX Ingress Controller to be ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

# Build and load Docker images
echo "Building and loading Docker images..."
./build-and-load.sh "${IMG_VERSION}" "${CLUSTER_NAME}"

# Replace image versions in manifests and Helm charts
echo "Replacing image versions in manifests and Helm charts..."
sed -i "s/${ACTUAL_IMG_VERSION}/${IMG_VERSION}/g" k8s/backend/deployment.yaml
sed -i "s/${ACTUAL_IMG_VERSION}/${IMG_VERSION}/g" k8s/frontend/deployment.yaml
sed -i "s/${ACTUAL_IMG_VERSION}/${IMG_VERSION}/g" k8s/helm/backend/values.yaml
sed -i "s/${ACTUAL_IMG_VERSION}/${IMG_VERSION}/g" k8s/helm/frontend/values.yaml

# Apply Kubernetes resources
case "$1" in
manifests)
  echo "Applying manifests..."
  apply_manifests
  ;;
helm)
  echo "Applying Helm charts..."
  apply_helm_charts
  ;;
*)
  get_help
  exit 1
  ;;
esac

echo "Deployment complete!"
echo "To check api logs: kubectl logs -n quotes-app -f deployment/quotes-api"
echo "To check server logs: kubectl logs -n quotes-app -f deployment/quotes-frontend"
echo "To check MySQL logs: kubectl logs -n quotes-app -f statefulset/quotes-db"
echo "To check NGINX ingress logs: kubectl logs -f -n ingress-nginx deployment/ingress-nginx-controller"
echo "-------------------------------------------------"
echo "To access the frontend, visit: http://quotes.local/"
echo "To access the API, visit: http://quotes.local/api/"
echo "Api Docs: http://quotes.local/api/docs"
echo "-------------------------------------------------"
echo "To delete the cluster, run: kind delete cluster --name ${CLUSTER_NAME}"
