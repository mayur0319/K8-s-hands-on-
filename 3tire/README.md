# Three-Tier Coder App

This folder contains a sample three-tier application with:
- `frontend` service serving a static UI with Nginx
- `backend` service running a Python Flask API
- `db` service running MySQL and initializing sample data

## Build images

```bash
cd K8-s-hands-on-/3tire

docker build -t coder-backend:latest ./backend
docker build -t coder-frontend:latest ./frontend
```

If you want to publish the images, replace the local names with your registry:

```bash
docker build -t myrepo/coder-backend:latest ./backend
docker build -t myrepo/coder-frontend:latest ./frontend
```

## Deploy to Kubernetes

```bash
kubectl apply -f ./k8s/3tier.yaml
```

## Access frontend

Open the frontend service at:

```bash
http://localhost:30080
```

## Notes

- Frontend calls the backend through the cluster DNS service `backend-service`.
- Backend reads data from the MySQL database on `db-service`.
- MySQL init SQL creates a sample `messages` row for the demo.
