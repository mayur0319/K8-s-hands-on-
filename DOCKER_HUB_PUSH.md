# Docker Hub Push Instructions

## Step 1: Prepare for Push

Make sure you've tested locally successfully:
```bash
# Run the local test script
chmod +x test-local.sh
./test-local.sh
```

---

## Step 2: Login to Docker Hub

```bash
# Login to Docker Hub
docker login

# You'll be prompted for:
# - Username: <your-dockerhub-username>
# - Password: <your-dockerhub-password>
```

---

## Step 3: Tag Your Image

Replace `<your-dockerhub-username>` with your actual Docker Hub username:

```bash
# Option A: Tag the existing image
docker tag k8s-app:v1 <your-dockerhub-username>/k8s-app:v1

# Option B: Build and tag directly
docker build -t <your-dockerhub-username>/k8s-app:v1 .
```

**Example:**
```bash
docker tag k8s-app:v1 mayur0319/k8s-app:v1
```

---

## Step 4: Push to Docker Hub

```bash
docker push <your-dockerhub-username>/k8s-app:v1
```

**Example:**
```bash
docker push mayur0319/k8s-app:v1
```

---

## Step 5: Verify Push

Visit your Docker Hub repository:
```
https://hub.docker.com/r/<your-dockerhub-username>/k8s-app
```

Or use CLI:
```bash
docker pull <your-dockerhub-username>/k8s-app:v1
```

---

## Complete Push Script

Save this as `push-to-hub.sh`:

```bash
#!/bin/bash

USERNAME="<your-dockerhub-username>"
IMAGE_NAME="k8s-app"
VERSION="v1"

echo "🐳 Docker Hub Push Script"
echo ""
echo "Username: $USERNAME"
echo "Image: $IMAGE_NAME:$VERSION"
echo ""

# Login
echo "📝 Logging in to Docker Hub..."
docker login

# Build
echo "🏗️  Building image..."
docker build -t $IMAGE_NAME:$VERSION .

# Tag
echo "🏷️  Tagging image..."
docker tag $IMAGE_NAME:$VERSION $USERNAME/$IMAGE_NAME:$VERSION

# Push
echo "⬆️  Pushing to Docker Hub..."
docker push $USERNAME/$IMAGE_NAME:$VERSION

echo "✅ Done! Image pushed to: https://hub.docker.com/r/$USERNAME/$IMAGE_NAME"
```

Make it executable and run:
```bash
chmod +x push-to-hub.sh
./push-to-hub.sh
```

---

## Update Kubernetes Deployment

After pushing, update your `deployment.yaml`:

```yaml
spec:
  containers:
  - name: sampleapp
    image: <your-dockerhub-username>/k8s-app:v1  # ← Update this
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker build -t name:tag .` | Build image |
| `docker login` | Login to Docker Hub |
| `docker tag source:tag dest:tag` | Tag for push |
| `docker push name:tag` | Push to registry |
| `docker pull name:tag` | Pull from registry |
| `docker images` | List local images |
| `docker ps -a` | List all containers |

---

## Troubleshooting

### "denied: requested access to the resource is denied"
- Make sure you're logged in: `docker login`
- Check username matches your Docker Hub username

### "image already exists"
- Use a different version tag: `v1.1`, `v2`, etc.
- Or tag with latest: `docker tag myapp:v1 username/myapp:latest`

### "Docker daemon is not running"
- Start Docker Desktop (macOS/Windows) or Docker service (Linux)

### Check push progress
```bash
docker push <username>/image:tag --verbose
docker inspect <username>/image:tag
```

---

## Verify Image in Kubernetes

After deploying to your cluster:

```bash
# Check pod status
kubectl get pods -l app=sampleapp

# Check ConfigMap is mounted
kubectl exec <pod-name> -- env | grep APP_CONFIG

# Check Secret is mounted
kubectl exec <pod-name> -- cat /mnt/secrets/secret.txt

# Test endpoints
kubectl port-forward pod/<pod-name> 3000:3000
curl http://localhost:3000/config
curl http://localhost:3000/secret
```
