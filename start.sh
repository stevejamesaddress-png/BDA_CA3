#!/bin/bash
# =====================================================
# File: start.sh
# Author: Steven James L00196960
# Starts Argo CD + MLflow installing as needed in each delegated script
# =====================================================

echo "staring argo cd..."
./install-argocd.sh
echo "Starting MLflow..."
./start-mlflow.sh

echo "Started"