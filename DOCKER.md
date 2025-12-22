# 🐳 Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker CLI

```bash
# Build image
docker build -t customer-churn-prediction:v1.0.0 .

# Run container
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  customer-churn-prediction:v1.0.0

# View logs
docker logs -f churn-prediction

# Stop container
docker stop churn-prediction
docker rm churn-prediction
```

## 📋 Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)

### Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install --cask docker
```

**Windows:**
Download from https://www.docker.com/products/docker-desktop

## 🏗️ Build Options

### Development Build
```bash
docker build -t churn-prediction:dev .
```

### Production Build (Optimized)
```bash
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t churn-prediction:v1.0.0 \
  --no-cache .
```

### Multi-platform Build
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t churn-prediction:v1.0.0 \
  --push .
```

## 🚀 Running the Container

### Basic Run
```bash
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  customer-churn-prediction:v1.0.0
```

### With Environment Variables
```bash
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  -e PORT=8000 \
  -e DEBUG=False \
  customer-churn-prediction:v1.0.0
```

### With Volume Mounts (Development)
```bash
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  -v $(pwd)/templates:/app/templates:ro \
  -v $(pwd)/best_model_pipeline.pkl:/app/best_model_pipeline.pkl:ro \
  customer-churn-prediction:v1.0.0
```

### With Restart Policy
```bash
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  --restart unless-stopped \
  customer-churn-prediction:v1.0.0
```

## 🔍 Container Management

### View Running Containers
```bash
docker ps
```

### View All Containers
```bash
docker ps -a
```

### View Logs
```bash
# Follow logs
docker logs -f churn-prediction

# Last 100 lines
docker logs --tail 100 churn-prediction

# With timestamps
docker logs -t churn-prediction
```

### Execute Commands in Container
```bash
# Interactive shell
docker exec -it churn-prediction /bin/bash

# Run Python script
docker exec churn-prediction python test_model.py

# Check health
docker exec churn-prediction curl http://localhost:8000/health
```

### Container Stats
```bash
docker stats churn-prediction
```

### Inspect Container
```bash
docker inspect churn-prediction
```

## 🧪 Testing the Container

### Health Check
```bash
curl http://localhost:8000/health
```

### Test Prediction
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "senior_citizen": "No",
    "under_30": "Yes",
    "dependents": "No",
    "referred_a_friend": "Yes",
    "paperless_billing": "Yes",
    "premium_tech_support": "No",
    "unlimited_data": "Yes",
    "multiple_lines": "No",
    "online_backup": "No",
    "device_protection_plan": "Yes",
    "streaming_tv": "Yes",
    "streaming_movies": "Yes",
    "streaming_music": "No",
    "tenure_in_months": 24.0,
    "avg_monthly_gb_download": 35.5,
    "monthly_charge": 85.50,
    "contract": "One Year",
    "payment_method": "Credit Card (automatic)",
    "offer": "Offer B",
    "internet_type": "Fiber Optic",
    "satisfaction_score": 4
  }'
```

### Access Web Interface
```
http://localhost:8000
```

### API Documentation
```
http://localhost:8000/docs
```

## 🏷️ Image Management

### List Images
```bash
docker images
```

### Tag Image
```bash
docker tag customer-churn-prediction:v1.0.0 yourusername/churn-prediction:v1.0.0
docker tag customer-churn-prediction:v1.0.0 yourusername/churn-prediction:latest
```

### Push to Docker Hub
```bash
# Login
docker login

# Push
docker push yourusername/churn-prediction:v1.0.0
docker push yourusername/churn-prediction:latest
```

### Pull from Docker Hub
```bash
docker pull yourusername/churn-prediction:v1.0.0
```

### Remove Image
```bash
docker rmi customer-churn-prediction:v1.0.0
```

## 🔧 Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs churn-prediction

# Check if port is in use
lsof -i :8000

# Try different port
docker run -d -p 8080:8000 customer-churn-prediction:v1.0.0
```

### Model Not Loading
```bash
# Check if model file exists in image
docker exec churn-prediction ls -lh best_model_pipeline.pkl

# Check logs for errors
docker logs churn-prediction | grep -i error
```

### Out of Memory
```bash
# Run with memory limit
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  --memory="512m" \
  --memory-swap="1g" \
  customer-churn-prediction:v1.0.0
```

### Slow Performance
```bash
# Check resource usage
docker stats churn-prediction

# Allocate more CPU
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  --cpus="2" \
  customer-churn-prediction:v1.0.0
```

## 🌐 Production Deployment

### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml churn-stack

# List services
docker service ls

# Scale service
docker service scale churn-stack_churn-prediction=3
```

### Using Kubernetes
See `k8s/` directory for Kubernetes manifests (if created)

### Using Cloud Platforms

**AWS ECS:**
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag customer-churn-prediction:v1.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:v1.0.0
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:v1.0.0
```

**Google Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/churn-prediction

# Deploy
gcloud run deploy churn-prediction \
  --image gcr.io/PROJECT-ID/churn-prediction \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Azure Container Instances:**
```bash
# Push to ACR
az acr login --name myregistry
docker tag customer-churn-prediction:v1.0.0 myregistry.azurecr.io/churn-prediction:v1.0.0
docker push myregistry.azurecr.io/churn-prediction:v1.0.0

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name churn-prediction \
  --image myregistry.azurecr.io/churn-prediction:v1.0.0 \
  --dns-name-label churn-prediction \
  --ports 8000
```

## 📊 Image Information

**Base Image:** python:3.11-slim  
**Final Size:** ~500-600 MB  
**Exposed Port:** 8000  
**Health Check:** Enabled  
**User:** Non-root (appuser)  

## 🔒 Security Best Practices

✅ Non-root user  
✅ Minimal base image (slim)  
✅ No unnecessary packages  
✅ Health checks enabled  
✅ .dockerignore configured  
✅ Environment variables for config  

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 8000 | Application port |
| DEBUG | False | Debug mode |
| MODEL_PATH | best_model_pipeline.pkl | Path to model file |

## 🎯 Performance Tips

1. **Use multi-stage builds** for smaller images
2. **Cache dependencies** by copying requirements.txt first
3. **Use .dockerignore** to exclude unnecessary files
4. **Run as non-root user** for security
5. **Set resource limits** in production
6. **Use health checks** for monitoring

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Best Practices for Python Docker Images](https://docs.docker.com/language/python/build-images/)

---

**Need help?** Check the logs with `docker logs -f churn-prediction`
