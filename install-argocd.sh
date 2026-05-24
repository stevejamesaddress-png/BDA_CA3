#!/bin/bash
# =====================================================
# File: install-argocd.sh
# Author: Steven James L00196960
# 
# One-click script to install Argo CD into Rancher Desktop Kubernetes
# Run this once to set up Argo CD.
# =====================================================

echo "=== Starting Argo CD installation ==="
NAMESPACE="argocd"

echo "Creating ${NAMESPACE} namespace..."
kubectl create namespace ${NAMESPACE} > /dev/null 2>&1 || true


echo "Installing Argo CD..."
kubectl apply -n ${NAMESPACE} -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl create clusterrolebinding argocd-application-controller-cluster-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=$NAMESPACE:argocd-application-controller 2>/dev/null || echo "ClusterRoleBinding already exists"
echo "Waiting for agro.."
kubectl wait --for=condition=established crd/applications.argoproj.io --timeout=90s

kubectl wait --for=condition=ready pod --all -n ${NAMESPACE} --timeout=300s

echo "Apply argo=cd.yaml definition"
kubectl apply -f k8s/argo-cd.yaml -n ${NAMESPACE}

echo "runing! "
kubectl get pods -n ${NAMESPACE}

echo "***** Argo CD done"
PASSWORD=$(kubectl -n ${NAMESPACE} get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo "Starting Argo UI//localhost:8080"
echo "Password : $PASSWORD"
pkill -f "kubectl port-forward"
kubectl port-forward svc/argocd-server -n ${NAMESPACE} 8080:443 2>&1 &

echo "Argo cd is hereo: https://localhost:8080"
echo "login with username 'admin' and the password above."
