
# =====================================================
# File: shutdown.sh
# Author: Steven James L00196960
# 
# Script to shut down the flask app and MLflow
# =====================================================

#!/bin/bash
NAMESPACE="argocd"

echo "*** stopping API ***"
kubectl delete deployment bda-ca3-api -n $NAMESPACE --ignore-not-found=true
kubectl delete service bda-ca3-api -n $NAMESPACE --ignore-not-found=true
sleep 2
echo "Shutdown complete."
kubectl delete namespace $NAMESPACE --force --grace-period=0
echo "deleted namespace $NAMESPACE"
echo "killing port forward"
pkill -f "kubectl port-forward"