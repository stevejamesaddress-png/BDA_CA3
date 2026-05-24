#build and runs the mlflow server in default namespace of K8s cluster 
#!/bin/bash
NAMESPACE="default"

kubectl apply -f k8s/deploy-mlflow.yaml -n $NAMESPACE
kubectl apply -f k8s/mlflow-service.yaml -n $NAMESPACE

echo "Waiting..."
kubectl wait --for=condition=ready pod -l app=mlflow -n $NAMESPACE --timeout=90s

echo "Status"
kubectl get pods -n $NAMESPACE -l app=mlflow
echo "Ready go to: http://localhost:5000"