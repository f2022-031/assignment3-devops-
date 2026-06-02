# DevOps Assignment 3

This project contains a complete containerized and Kubernetes-ready setup with:

- `Flask API` backend
- `MySQL` database
- `Nginx` reverse proxy
- `Docker Compose` for local orchestration
- `Kubernetes` manifests for deployment
- `GitHub Actions` CI/CD workflow for build and image publishing

## Project Structure

```text
.
├── app
│   ├── docker-compose.yml
│   ├── flask-api
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── nginx
│       ├── Dockerfile
│       └── nginx.conf
├── k8s
│   ├── namespace.yml
│   ├── mysql-secret.yml
│   ├── mysql-pv.yml
│   ├── mysql-pvc.yml
│   ├── mysql-deployment.yml
│   ├── mysql-service.yml
│   ├── flask-configmap.yml
│   ├── flask-deployment.yml
│   ├── flask-service.yml
│   ├── nginx-configmap.yml
│   ├── nginx-deployment.yml
│   └── nginx-service.yml
├── .github/workflows/ci-cd.yml
├── .gitignore
├── README.md
└── start.sh
```

## Local Run with Docker Compose

From repository root:

```bash
./start.sh
```

Then test:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
```

## Kubernetes Deployment

Apply manifests in order:

```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/mysql-secret.yml
kubectl apply -f k8s/mysql-pv.yml
kubectl apply -f k8s/mysql-pvc.yml
kubectl apply -f k8s/mysql-deployment.yml
kubectl apply -f k8s/mysql-service.yml
kubectl apply -f k8s/flask-configmap.yml
kubectl apply -f k8s/flask-deployment.yml
kubectl apply -f k8s/flask-service.yml
kubectl apply -f k8s/nginx-configmap.yml
kubectl apply -f k8s/nginx-deployment.yml
kubectl apply -f k8s/nginx-service.yml
```

Check status:

```bash
kubectl get all -n devops-assignment
```

Access app (NodePort service):

```bash
http://<NODE_IP>:30080
```

## CI/CD Workflow

Workflow file: `.github/workflows/ci-cd.yml`

It performs:
- Python dependency installation
- Flask app import smoke test
- Docker image build (Flask + Nginx)
- Docker Hub push on `main` branch push events

Required GitHub Secrets:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Notes

- Update image names in `k8s/flask-deployment.yml` to your own registry/image path.
- MySQL credentials are stored in Kubernetes secret (base64 encoded values).
