#!/usr/bin/env bash
set -euo pipefail

MANIFEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "Error: kubectl is not installed or not in PATH."
  exit 1
fi

files=(
  "namespace.yaml"
  "pv-pvc-mysql.yaml"
  "configmap-mysql-init.yaml"
  "deployment-db.yaml"
  "service-db.yaml"
  "deployment-backend.yaml"
  "service-backend.yaml"
  "deployment-frontend.yaml"
  "service-frontend.yaml"
  "networkpolicy-3tier.yaml"
)

for file in "${files[@]}"; do
  echo "Applying ${file}..."
  kubectl apply -f "${MANIFEST_DIR}/${file}"
done

echo "All manifests applied successfully."
