# Docker Setup and Usage Guide

This guide explains how to set up Docker on macOS without Docker Desktop and how to build and run the Safe LLM Bot application using Docker.

## Prerequisites

- macOS system
- Homebrew package manager

## Docker Setup (without Docker Desktop)

### 1. Install Required Tools

```bash
# Install Docker CLI
brew install docker

# Install Lima (required for Colima)
brew install lima

# Install Colima (lightweight Docker daemon)
brew install colima
```

### 2. Start Colima

```bash
# Add Homebrew binaries to PATH
export PATH="/opt/homebrew/bin:$PATH"

# Start Colima (this will download and start a Linux VM)
colima start
```

**Note**: The first start will take some time as it downloads the VM image.

### 3. Verify Installation

```bash
# Check Docker version
docker --version

# Test Docker connection
docker ps
```

## Building the Application

### 1. Build Docker Image

From the project root directory:

```bash
# Ensure PATH includes Homebrew binaries
export PATH="/opt/homebrew/bin:$PATH"

# Build the image (ARM64 for local testing)
docker build -t safebotapi .
```

### 2. Cross-Platform Build for Azure

**Important**: ARM64 images built on Apple Silicon Macs won't run on Azure's x86_64 infrastructure. For Azure deployment, use Azure Container Registry's cloud build:

```bash
# Build x86_64 image in Azure Container Registry
az acr build --registry <your-registry> --image safebotapi:latest --platform linux/amd64 .
```

This builds the image on Azure's x86_64 infrastructure, ensuring compatibility.

### 2. Verify Build

```bash
# List Docker images
docker images | grep safebotapi
```

## Running the Application

### 1. Run Locally (for testing)

```bash
# Run the container locally
docker run -p 8000:8000 --env-file .env safebotapi
```

The application will be available at `http://localhost:8000`

### 2. Test Health Endpoint

```bash
# Test the health check
curl http://localhost:8000/api/health
```

Expected response: `{"status":"ok"}`

## Deployment

### Local Registry Push (for testing)

```bash
# Tag for your container registry
docker tag safebotapi your-registry/safebotapi:latest

# Login to your registry
docker login your-registry

# Push the image
docker push your-registry/safebotapi:latest
```

### Azure Container Registry (Recommended)

For Azure deployment, use ACR's cloud build to ensure x86_64 compatibility:

```bash
# Login to Azure Container Registry
az acr login --name <your-registry>

# Build and push directly to ACR (x86_64)
az acr build --registry <your-registry> --image safebotapi:latest --platform linux/amd64 .
```

**Note**: See `AZURE_README.md` for complete Azure deployment guide.

## Troubleshooting

### Common Issues

1. **"Cannot connect to Docker daemon"**
   - Ensure Colima is running: `colima status`
   - If not running: `colima start`

2. **"limactl: executable file not found"**
   - Add Homebrew to PATH: `export PATH="/opt/homebrew/bin:$PATH"`
   - Add this line to your `~/.zshrc` for persistence

3. **"docker: command not found"**
   - Ensure Docker CLI is installed: `brew install docker`
   - Check PATH includes `/opt/homebrew/bin`

4. **"docker-credential-desktop: executable file not found" when logging into registries**
   - This happens when Docker config tries to use Docker Desktop's credential helper
   - Fix by updating `~/.docker/config.json`:
   ```bash
   echo '{
           "auths": {},
           "currentContext": "colima"
   }' > ~/.docker/config.json
   ```
   - Then retry your login command (e.g., `az acr login --name yourregistry`)

### Stopping Colima

When you're done working with Docker:

```bash
# Stop Colima (saves resources)
colima stop
```

## Environment Variables

The application requires these environment variables (stored in `.env`):

```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_CONTENT_SAFETY_ENDPOINT=your_endpoint
AZURE_CONTENT_SAFETY_KEY=your_key
```

## Dockerfile Overview

The current Dockerfile:
- Uses Python 3.10 slim base image
- Installs dependencies from `requirements.txt`
- Copies application code
- Exposes port 8000
- Runs the FastAPI app with Uvicorn

## Docker Image Storage

### Where Images Are Stored

Your Docker images are stored in **Colima's virtual machine**:

- **Physical location on Mac**: `~/.colima/_lima/default/`
- **Inside the VM**: `/var/lib/docker/` (Linux filesystem)
- **Docker socket**: `unix:///Users/zvezdanprotic/.colima/default/docker.sock`

### Storage Details

When you run `docker images`, you'll see something like:
```
REPOSITORY   TAG         IMAGE ID       CREATED         SIZE
safebotapi   latest      9ee0586c50c4   2 minutes ago   546MB
```

### Important Notes

- Images exist **only locally** in the Colima VM
- If you stop/delete Colima, you'll **lose the images**
- Images are **not directly accessible** from macOS filesystem
- Total storage used can be checked with: `docker system df`

### Backup/Export Images

To save an image as a file for backup or transfer:

```bash
# Export image to tar file
docker save safebotapi:latest -o safebotapi.tar

# Import image from tar file (on another machine)
docker load -i safebotapi.tar
```

### Clean Up Storage

```bash
# Remove unused images
docker image prune

# Remove all unused containers, networks, images
docker system prune

# Remove everything (including volumes)
docker system prune -a --volumes
```

## Useful Commands

```bash
# Start Colima
colima start

# Check Colima status
colima status

# Build image
docker build -t safebotapi .

# Run container
docker run -p 8000:8000 --env-file .env safebotapi

# List images
docker images

# Check storage usage
docker system df

# List running containers
docker ps

# Stop container
docker stop <container_id>

# Remove image
docker rmi safebotapi

# Export image to file
docker save safebotapi:latest -o safebotapi.tar

# Import image from file
docker load -i safebotapi.tar

# Clean up unused images
docker image prune

# Stop Colima
colima stop
```

## Production Considerations

1. **Security**: Don't include `.env` files in the image for production
2. **Multi-stage builds**: Consider using multi-stage builds to reduce image size
3. **Health checks**: The `/api/health` endpoint can be used for container health checks
4. **Resource limits**: Set appropriate CPU and memory limits when running containers
5. **Logging**: Configure proper logging for production deployments