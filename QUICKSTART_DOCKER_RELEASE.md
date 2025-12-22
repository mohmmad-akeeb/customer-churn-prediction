# 🚀 Quick Start: Docker & Git Release v1.0.0

## 📦 Step 1: Test Docker Build

```bash
# Build the Docker image
docker build -t customer-churn-prediction:v1.0.0 .

# This should take 2-3 minutes
# Expected output: Successfully built <image-id>
```

## 🧪 Step 2: Test Docker Container

```bash
# Run the container
docker run -d \
  --name churn-test \
  -p 8000:8000 \
  customer-churn-prediction:v1.0.0

# Wait 5 seconds for startup
sleep 5

# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status":"healthy","model_loaded":true}

# Test web interface
curl -I http://localhost:8000/

# Expected: HTTP/1.1 200 OK

# View logs
docker logs churn-test

# Stop and remove test container
docker stop churn-test
docker rm churn-test
```

## 🏷️ Step 3: Create Git Tag v1.0.0

### Option A: Use the Release Script (Easiest)

```bash
# Make script executable (if not already)
chmod +x release.sh

# Run the release script
./release.sh

# Follow the prompts:
# - It will check for uncommitted changes
# - Create the v1.0.0 tag
# - Ask if you want to push to remote
```

### Option B: Manual Git Tagging

```bash
# 1. Check status
git status

# 2. Commit any changes
git add .
git commit -m "Release v1.0.0 - Customer Churn Prediction App"

# 3. Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0

Customer Churn Prediction Web Application

Features:
- FastAPI backend with Random Forest ML model
- Modern dark-themed responsive UI
- Docker support for easy deployment
- Real-time predictions with probability scores
- Comprehensive API documentation

Tech Stack:
- FastAPI 0.104.1
- scikit-learn 1.5.2
- Python 3.11
- Docker & Docker Compose
"

# 4. View the tag
git show v1.0.0

# 5. Push to remote
git push origin main
git push origin v1.0.0
```

## 🐳 Step 4: Docker Compose (Alternative)

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📤 Step 5: Push to Docker Hub (Optional)

```bash
# 1. Login to Docker Hub
docker login
# Enter your username and password

# 2. Tag your image
docker tag customer-churn-prediction:v1.0.0 YOUR_DOCKERHUB_USERNAME/churn-prediction:v1.0.0
docker tag customer-churn-prediction:v1.0.0 YOUR_DOCKERHUB_USERNAME/churn-prediction:latest

# 3. Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/churn-prediction:v1.0.0
docker push YOUR_DOCKERHUB_USERNAME/churn-prediction:latest

# Now anyone can pull your image:
# docker pull YOUR_DOCKERHUB_USERNAME/churn-prediction:v1.0.0
```

## ✅ Verification Checklist

After completing the steps above, verify:

- [ ] Docker image builds successfully
- [ ] Container runs without errors
- [ ] Health check returns healthy status
- [ ] Web interface accessible at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Git tag v1.0.0 created
- [ ] Tag pushed to remote repository
- [ ] (Optional) Docker image pushed to Docker Hub

## 🎯 Quick Commands Summary

```bash
# Docker Build
docker build -t customer-churn-prediction:v1.0.0 .

# Docker Run
docker run -d -p 8000:8000 --name churn-app customer-churn-prediction:v1.0.0

# Docker Compose
docker-compose up -d

# Git Tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# View Tags
git tag -l

# View Tag Details
git show v1.0.0
```

## 🔍 Troubleshooting

### Docker build fails
```bash
# Check Docker is running
docker --version

# Clean build cache
docker builder prune

# Rebuild without cache
docker build --no-cache -t customer-churn-prediction:v1.0.0 .
```

### Container won't start
```bash
# Check logs
docker logs churn-app

# Check if port 8000 is in use
lsof -i :8000

# Use different port
docker run -d -p 8080:8000 customer-churn-prediction:v1.0.0
```

### Git tag already exists
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Recreate tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## 📚 Next Steps

1. **Create GitHub Release**
   - Go to: https://github.com/YOUR_USERNAME/churn-prediction/releases/new
   - Select tag: v1.0.0
   - Add release notes
   - Publish

2. **Deploy to Production**
   - See DEPLOYMENT.md for platform-specific guides
   - Render.com, Railway.app, or Fly.io recommended

3. **Share Your Work**
   - Update README with production URL
   - Share on LinkedIn/Twitter
   - Add to portfolio

## 🎉 Success!

You now have:
- ✅ Dockerized application
- ✅ Git tag v1.0.0
- ✅ Ready for deployment
- ✅ Shareable Docker image

**Time to deploy:** ~10 minutes  
**Difficulty:** Easy

---

**Need help?** Check:
- DOCKER.md for detailed Docker guide
- RELEASE_CHECKLIST.md for complete release process
- DEPLOYMENT.md for deployment options
