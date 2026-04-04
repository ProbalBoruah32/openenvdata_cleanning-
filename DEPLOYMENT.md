# Deployment Guide for Data Cleaning OpenEnv Environment

Complete instructions for deploying to Hugging Face Spaces and other cloud platforms.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Setup](#docker-setup)
3. [Hugging Face Spaces Deployment](#hugging-face-spaces-deployment)
4. [AWS Deployment (Optional)](#aws-deployment-optional)
5. [Validation & Testing](#validation--testing)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv)

### Setup Steps

```bash
# 1. Clone repository
git clone <your-repo-url>
cd data-cleaning-env

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\Activate.ps1

# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment configuration
cp .env.example .env

# 6. Edit .env with your settings
# Add your OPENAI_API_KEY and HF_TOKEN

# 7. Run the application
uvicorn app:app --reload --port 8000
```

### Testing Locally

```bash
# In a new terminal window:
curl http://localhost:8000/reset
curl http://localhost:8000/tasks
python inference.py
```

---

## Docker Setup

### Build Docker Image

```bash
# Build the image
docker build -t data-cleaning-env:latest .

# Or build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t data-cleaning-env:latest .
```

### Run Docker Container

```bash
# Basic run
docker run -p 8000:8000 data-cleaning-env:latest

# Run with environment file
docker run -p 8000:8000 --env-file .env data-cleaning-env:latest

# Run with environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="sk-..." \
  -e HF_TOKEN="hf_..." \
  -e ENVIRONMENT="production" \
  data-cleaning-env:latest

# Run in background
docker run -d -p 8000:8000 \
  --name data-cleaning \
  --env-file .env \
  data-cleaning-env:latest

# View logs
docker logs -f data-cleaning

# Stop container
docker stop data-cleaning
```

### Docker Compose (Recommended for Local Testing)

```bash
# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Verify Docker Deployment

```bash
# Inside container or from host:
curl http://localhost:8000/reset
curl http://localhost:8000/tasks

# Run inference
docker exec -it data-cleaning python inference.py
```

---

## Hugging Face Spaces Deployment

### Step 1: Create HF Repository

```bash
# Login to Hugging Face
huggingface-cli login

# Create a new Space repository
# Visit: https://huggingface.co/new-space
# - Name: data-cleaning-env
# - License: openrail
# - Space type: Docker
```

### Step 2: Clone and Setup

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/data-cleaning-env
cd data-cleaning-env

# Copy files from your local repo
cp -r /path/to/your/repo/* .

# Ensure Dockerfile exists
ls -la Dockerfile

git add .
git commit -m "Initial commit: Data Cleaning Environment"
git push
```

### Step 3: Configure Secrets

In HF Spaces web interface:

1. Go to Settings tab
2. Click "Add secrets"
3. Add the following secrets:
   - `OPENAI_API_KEY`: your-openai-api-key
   - `HF_TOKEN`: your-huggingface-token  
   - `ENVIRONMENT`: production
   - `LOG_LEVEL`: INFO

### Step 4: Dockerfile Configuration

The Dockerfile is automatically detected by HF Spaces. Ensure it:
- Uses `FROM python:3.11-slim`
- Installs `requirements.txt`
- Exposes port 8000
- Has `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`

### Step 5: Verify Deployment

```bash
# Wait 5-10 minutes for build to complete
# Check Space status in HF interface

# Test endpoints
curl https://YOUR_USERNAME-data-cleaning-env.hf.space/reset
curl https://YOUR_USERNAME-data-cleaning-env.hf.space/tasks

# Test inference (may take longer due to cold start)
curl https://YOUR_USERNAME-data-cleaning-env.hf.space/run-inference
```

### Step 6: Monitor & Debug

In HF Spaces interface:
- View build logs in Settings
- Check application logs in Live logs tab
- Use "Restart space" if needed
- Set env vars without rebuilding using Settings

---

## AWS Deployment (Optional)

### Using AWS App Runner

```bash
# 1. Push Docker image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag data-cleaning-env:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/data-cleaning-env:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/data-cleaning-env:latest

# 2. Create App Runner service via AWS Console or CLI
aws apprunner create-service \
  --service-name data-cleaning-env \
  --source-configuration '{"ImageRepository":{"ImageIdentifier":"YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/data-cleaning-env:latest","ImageRepositoryType":"ECR"}}'
```

### Using AWS ECS

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name data-cleaning-env

# 2. Push image (same as above)

# 3. Create ECS task definition JSON (task-definition.json)
# 4. Register task
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 5. Create service
aws ecs create-service \
  --cluster default \
  --service-name data-cleaning-env \
  --task-definition data-cleaning-env \
  --desired-count 1
```

---

## Validation & Testing

### Pre-Deployment Validation

```bash
# 1. Run validator script
python validator.py

# Expected output:
# [SUCCESS] ALL CHECKS PASSED - READY FOR SUBMISSION

# 2. Test inference script
python inference.py

# Expected output:
# [START]
# task: uploaded_data_cleaning
# [STEP]
# action: fill_missing
# reward: 0.3
# ...
# [END]
# score: 1.0

# 3. Test API endpoints
curl -X GET http://localhost:8000/reset
curl -X GET http://localhost:8000/tasks
curl -X GET http://localhost:8000/state

# 4. Build Docker image
docker build -t data-cleaning-env:test .
```

### Load Testing

```bash
# Using Apache Bench (example)
ab -n 100 -c 10 http://localhost:8000/reset

# Using wrk (if installed)
wrk -t12 -c400 -d30s http://localhost:8000/reset

# Using python requests
python -c "
import requests
import time

for i in range(10):
    start = time.time()
    r = requests.get('http://localhost:8000/reset')
    elapsed = time.time() - start
    print(f'Request {i+1}: {r.status_code} ({elapsed:.2f}s)')
"
```

---

## Monitoring & Logging

### Local Monitoring

```bash
# View FastAPI logs in real-time
uvicorn app:app --log-level debug --reload

# Capture logs to file
uvicorn app:app > app.log 2>&1 &
tail -f app.log
```

### Docker Monitoring

```bash
# View container logs
docker logs -f data-cleaning

# Monitor resource usage
docker stats data-cleaning

# Inspect container
docker inspect data-cleaning
```

### Application Metrics

```bash
# Check endpoints directly
curl http://localhost:8000/metrics  # If Prometheus is enabled

# Get environment info
curl http://localhost:8000/health

# Check task results
curl http://localhost:8000/tasks | jq .summary
```

---

## Scaling & Performance

### Recommendations

1. **For Development**:
   - Single instance with limited resources
   - Set max_workers=1 in uvicorn

2. **For Production**:
   - Use multiple workers: `uvicorn app:app --workers 4`
   - Load balancer in front
   - Monitor CPU/memory usage

3. **For High Traffic**:
   - Use gunicorn with worker class
   - Enable caching where possible
   - Consider horizontal scaling

### Uvicorn Configuration

```python
# For optimal performance:
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --loop uvloop \
  --http httptools
```

---

## Troubleshooting

### Issue: Port 8000 Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Solution: Use different port
uvicorn app:app --port 8001
```

### Issue: Docker Build Fails

```bash
# Check requirements.txt
pip freeze > requirements.txt

# Rebuild without cache
docker build --no-cache -t data-cleaning-env:latest .

# Check Dockerfile syntax
docker build --progress=plain -t data-cleaning-env:latest .
```

### Issue: API Responds with 500 Error

```bash
# Check logs
docker logs data-cleaning

# Check environment variables
docker inspect data-cleaning | grep "Env"

# Verify config
curl http://localhost:8000/health

# Test locally first
python -c "from app import app; print('Import successful')"
```

### Issue: Inference Script Timeout

```bash
# Reduce complexity
python -c "from env.tasks import get_tasks; print(len(get_tasks()))"

# Run with timeout wrapper
timeout 300 python inference.py

# Check system resources
top  # macOS/Linux
taskmgr  # Windows
```

### Issue: OPENAI_API_KEY Not Found

```bash
# Verify environment variable
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows

# Set it manually
export OPENAI_API_KEY="sk-..."  # Linux/Mac
set OPENAI_API_KEY=sk-...  # Windows

# Or add to .env file
echo "OPENAI_API_KEY=sk-..." >> .env
```

---

## Rollback Procedures

### Docker/Container

```bash
# Stop current container
docker stop data-cleaning

# Remove current container
docker rm data-cleaning

# Run previous version
docker run -d -p 8000:8000 \
  --name data-cleaning \
  --env-file .env \
  data-cleaning-env:previous
```

### HF Spaces

```bash
# Via git
git revert HEAD
git push

# Or via GUI
# Go to Settings -> Restart from previous commit
```

---

## Support & Resources

- GitHub Issues: <your-repo-url>/issues
- Email: your-email@example.com
- Documentation: README.md
- OpenEnv Spec: openenv.yaml

---

## Appendix: Environment Variables Reference

```
OPENAI_API_KEY     [REQUIRED] OpenAI API key
HF_TOKEN           [OPTIONAL] Hugging Face token
API_BASE_URL       [OPTIONAL] API base URL (default: http://localhost:8000)
MODEL_NAME         [OPTIONAL] Model name (default: gpt-3.5-turbo)
ENVIRONMENT        [OPTIONAL] Environment mode (default: development)
DEBUG              [OPTIONAL] Debug mode (default: false)
LOG_LEVEL          [OPTIONAL] Log level (default: INFO)
HOST               [OPTIONAL] Server host (default: 0.0.0.0)
PORT               [OPTIONAL] Server port (default: 8000)
```

---

End of Deployment Guide
