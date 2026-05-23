## **MLOps pipeline - High Level Architecture**

The assignment requires a complete MLOps pipeline that will automatically train, test, package, and deploy a small machine learning model as a web application. The architecture is built around three layers , each with a distinct responsibility.

**Automation Layer – GitHub Actions**

GitHub Actions is responsible for all automation. It monitors the repository and triggers actions in three key areas:

- Automatically runs Continuous Integration (ci.yml)
- Triggers model retraining when new training data is available (train-ct.yml)
- Packages the application into a Docker image for Continuous Delivery (deploy.yml)

The deploy.yml workflow updates the Kubernetes manifest file (k8s/deployment.yaml) with the new Docker image tag and commits the change back to the GitHub repository. In a full production system, a complete integration test that calls the Flask REST API endpoint would also be added to validate the full prediction flow before deployment.

Docker images are stored in GitHub Container Registry (GHCR), which integrates natively with GitHub Actions and requires no additional authentication setup.

**Layer Interface:** Git + Kubernetes manifest file.

**Deployment Layer – Argo CD + Rancher Desktop Kubernetes**

Argo CD is responsible for orchestrating the deployment into the runtime environment. It constantly watches the GitHub repository for changes to the Kubernetes manifests. When the deploy.yml workflow updates k8s/deployment.yaml with a new Docker image tag, Argo CD automatically detects the change and deploys the new version to the Kubernetes cluster running on Rancher Desktop. It manages rolling updates and health checks to ensure minimal downtime.

**Layer Interface:** Git + Kubernetes manifest file. The deploy.yml workflow updates k8s/deployment.yaml and commits the change.

**Application Layer – Docker and Flask**

The Flask web application is the user-facing part of the system. It provides a simple web-based interface where users can input flower measurements and receive a prediction. The entire application, including the trained model, is packaged inside a Docker container so it runs reliably on any machine and inside the Kubernetes cluster.

**Layer Interface:** Docker container running as a Kubernetes Pod, exposed to users through a Kubernetes Service on a specific port 9292.

### **Branching Strategy**

We use a simple GitHub Flow branching strategy. All development work happens on short lived feature branches. Changes are submitted via Pull Requests, which automatically trigger the CI workflow. Once approved and merged into main, the Continuous Delivery and Continuous Training workflows are triggered. The Docker image is always tagged main. This avoids more complex versioning system while ensuring the latest approved version is always deployed.

Devlopment Plan (Remove Later) key Development phases

**Phase 1 – Model + CI**

**Phase 2 – Flask + Docker** (next)

**Phase 3 – Full Pipeline + Argo CD** (later)

**Source**

Gift, N. & Deza, A., 2021. _Practical MLOps: Operationalizing Machine Learning Models_ . Sebastopol, CA: O’Reilly Media
