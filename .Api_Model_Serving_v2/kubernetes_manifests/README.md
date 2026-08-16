# Kubernetes - Fases 1 e 2 (API + MongoDB)

Este pacote cria manifests novos para fases 1 e 2 sem alterar os manifests anteriores.

## O que este pacote entrega

- Namespace dedicado (`picpay-ml`)
- ConfigMap da API com variaveis de ambiente para NoSQL
- Secret MongoDB (arquivo de exemplo + script de criacao)
- MongoDB em StatefulSet com volume persistente
- Deployment da API com liveness/readiness
- Services internos da API e do MongoDB
- Kustomization para aplicacao em lote

## Observacoes importantes

- A API atual ainda persiste metadados em JSON local; estes manifests deixam o ambiente pronto para a migracao de fase 1.
- Sem alterar o codigo da API, a readiness usa `/health-check/`.

## Pre-requisitos

- Cluster local ativo (kind ou minikube)
- kubectl configurado no contexto correto
- Imagem `picpay-model-api:latest` disponivel no runtime do cluster

## Como aplicar

1. Tornar scripts executaveis:

```bash
chmod +x 10-create-secret.sh 11-apply-phases1-2.sh
```

2. Ajustar credenciais (opcional):

```bash
export MONGO_INITDB_ROOT_USERNAME=admin
export MONGO_INITDB_ROOT_PASSWORD='admin1234'
```

3. Aplicar tudo:

```bash
./11-apply-phases1-2.sh
```

## Validacao

```bash
kubectl get all -n picpay-ml
kubectl get pvc -n picpay-ml
kubectl logs -n picpay-ml deploy/model-serving-api
```

## Acesso local a API

```bash
kubectl -n picpay-ml port-forward svc/model-serving-api 8000:80
curl http://localhost:8000/health-check/
```

## Arquivos criados

- `00-namespace.yaml`
- `01-configmap-api.yaml`
- `02-secret-mongodb.example.yaml`
- `03-mongodb-service.yaml`
- `04-mongodb-statefulset.yaml`
- `05-api-deployment.yaml`
- `06-api-service.yaml`
- `kustomization.yaml`
- `10-create-secret.sh`
- `11-apply-phases1-2.sh`