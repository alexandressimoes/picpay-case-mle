#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="picpay-ml"
SECRET_NAME="mongodb-auth"

: "${MONGO_INITDB_ROOT_USERNAME:=admin}"
: "${MONGO_INITDB_ROOT_PASSWORD:=admin1234}"

MONGODB_URI="mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/picpay_metadata?authSource=admin"

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

kubectl -n "${NAMESPACE}" create secret generic "${SECRET_NAME}" \
  --from-literal=MONGO_INITDB_ROOT_USERNAME="${MONGO_INITDB_ROOT_USERNAME}" \
  --from-literal=MONGO_INITDB_ROOT_PASSWORD="${MONGO_INITDB_ROOT_PASSWORD}" \
  --from-literal=MONGODB_URI="${MONGODB_URI}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret ${SECRET_NAME} aplicado no namespace ${NAMESPACE}."