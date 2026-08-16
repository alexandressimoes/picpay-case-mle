# API de Model Serving 
Readme principal sobre uso da API de model serving utilizando FastAPI e spaCy. Contém informações sobre endpoints, payloads, requisitos técnicos e boas práticas esperadas para o desenvolvimento do micro serviço.

## Passo a Passo de uso
1. Clone o repositório e navegue até a pasta `Api_Model_Serving`.

2. Ir para a raiz do repositório
`cd /home/alexandre/Documents/picpay-case-mle`

3. Buildar a imagem
```bash
docker build -f Api_Model_Serving/Dockerfile -t picpay-model-api .
```

4. Rodar o container
```bash
docker run --rm -d --name picpay-model-api -p 8000:80 picpay-model-api
```

5. Validar se a API subiu
```bash
curl http://localhost:8000/health-check/
```

Resposta esperada:
{"status":"healthy"}

6. Testar endpoints principais
Carregar modelo:
```bash
curl -X POST http://localhost:8000/load/ -H "Content-Type: application/json" -d "{"model":"en_core_web_sm"}"
```

Predição:
```bash
curl -X POST http://localhost:8000/predict/ -H "Content-Type: application/json" -d "{"text":"Apple announced a new product in California.","model":"en_core_web_sm"}"
```

Listar modelos:
```bash
curl http://localhost:8000/list-models/
```

7. Parar o container quando terminar
```bash
docker stop picpay-model-api
```
