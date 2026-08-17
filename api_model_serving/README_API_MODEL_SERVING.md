# Micro Serviço de Model Serving

## Descrição do problema

Este diretório contém a solução do problema de criar um micro serviço de NLP para serving de modelos spaCy.

Objetivos principais:
- disponibilizar endpoints HTTP para carga de modelo e inferência de entidades
- manter registro de modelos carregados
- registrar transações de predição
- permitir execução local, via Docker e validação com testes automatizados

## Estrutura principal

- app/main.py: API FastAPI e definição das rotas
- app/modules/model_manager.py: regras de carga, inferência e persistência local
- app/schemas/schemas.py: contratos de request/response
- tests/test_api_basic.py: testes básicos da API
- Dockerfile: execução containerizada

## Pré-requisitos

- Python 3.14+
- Dependências instaladas no ambiente (`uv sync` ou `pip install -r requirements.txt`)
- Docker

## Execução com Docker
Passos necessários para executar a API em container:

1. Na raiz do repositório, faça o build:
```bash
docker build -f api_model_serving/Dockerfile -t picpay-model-api .
```

2. Rode o container:
```bash
docker run --rm -d --name picpay-model-api -p 8000:80 picpay-model-api
```
Se tiver uma versão antiga rodando, limpe antes:

```bash
docker rm -f picpay-model-api 2>/dev/null || true
```

3. Pare o container ao final:
```bash
docker stop picpay-model-api
```

## Execução local (sem Docker)
1. Acesse a raiz do repositório:
```bash
cd picpay-case-mle
```

2. Inicie a API:
```bash
cd api_model_serving/app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Verifique saúde:
```bash
curl http://localhost:8000/health-check/
```

Resposta esperada:
```json
{"status":"healthy"}
```



## Teste funcional da API (smoke test)

1. Carregar modelo:
```bash
curl -X POST http://localhost:8000/load/ \
	-H "Content-Type: application/json" \
	-d '{"model":"en_core_web_sm"}'
```

### 3.2 Realizar predição

```bash
curl -X POST http://localhost:8000/predict/ \
	-H "Content-Type: application/json" \
	-d '{"text":"Apple announced a new product in California costing 1000 dollars.","model":"en_core_web_sm"}'
```

3. Listar modelos:
```bash
curl http://localhost:8000/list-models/
```

4. Listar predições:
```bash
curl http://localhost:8000/list/
```

## Testes automatizados (pytest)

Na raiz do repositório:
```bash
python -m pytest api_model_serving/tests -q
```

Cobertura básica atual:
- root e health-check
- load (sucesso e payload inválido)
- predict (sucesso e erro de negócio)
- list e list-models
- delete-model (sucesso e não encontrado)
