#!/usr/bin/env bash
set -euo pipefail

MANIFEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl nao encontrado no PATH" >&2
  exit 1
fi

"${MANIFEST_DIR}/10-create-secret.sh"

kubectl apply -k "${MANIFEST_DIR}"

echo "Aguardando MongoDB ficar pronto..."
kubectl -n picpay-ml rollout status statefulset/mongodb --timeout=240s

echo "Aguardando API ficar pronta..."
kubectl -n picpay-ml rollout status deployment/model-serving-api --timeout=240s

echo "Fases 1 e 2 aplicadas com sucesso."