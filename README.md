# PicPay Case MLE

Este repositório reúne as entregas de dois problemas propostos no processo seletivo.

Importante:
- A pasta .Api_Model_Serving_v2 foi desconsiderada desta organização, por se tratar de uma proposta de evolução arquitetural para a API de Model Serving atual.

## Estrutura do projeto

```text
picpay-case-mle/
├── .gitignore
├── .venv/
├── __init__.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── README.md
├── api_model_serving/
│   ├── Dockerfile
│   ├── README_API_MODEL_SERVING.md
│   ├── api_requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   └── model_manager.py
│   │   ├── models/
│   │   │   ├── model_registry.json
│   │   │   ├── predictions_registry.json
│   │   │   ├── en_core_web_sm/
│   │   │   └── pt_core_news_sm/
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── schemas.py
│   └── tests/
│       ├── conftest.py
│       ├── local_test_example.py
│       └── test_api_basic.py
├── pokeapi_spark/
│   ├── README_POKEAPI.md
│   ├── pokemon_spark.ipynb
│   └── data/
│       ├── raw/
│       └── trusted/
├── .Api_Model_Serving_v2/
│   └── ...
└── .pytest_cache/
```

### Descrição da estrutura

- `api_model_serving/`: contém a solução principal do microserviço de model serving em FastAPI.
  - `app/`: código da aplicação, rotas, módulos e schemas.
  - `app/modules/`: lógica de carregamento do modelo, predição e gerenciamento de registros.
  - `app/models/`: modelos spaCy baixados localmente e arquivos de registro.
  - `app/schemas/`: definição dos payloads de entrada e saída da API.
  - `tests/`: testes automatizados para validar os endpoints e o comportamento esperado.
  - `Dockerfile`: configuração para executar a API em container.

- `pokeapi_spark/`: contém a análise com PokeAPI e Spark.
  - `pokemon_spark.ipynb`: notebook para coleta, transformação e exploração dos dados.
  - `data/raw/`: dados brutos coletados da API.
  - `data/trusted/`: dados processados e prontos para análise.

- `.Api_Model_Serving_v2/`: versão alternativa/experimental da API, com abordagem de evolução arquitetural e persistência em MongoDB.

- `pyproject.toml`, `requirements.txt` e `uv.lock`: configuram as dependências e a execução do projeto.

## Leitura Necessária

Para executar ou entender cada entrega, consulte primeiro os READMEs das pastas:
- api_model_serving/README_API_MODEL_SERVING.md
- pokeapi_spark/README_POKEAPI.md

## Organização por problema

### 1. Análise de Dados com PokeAPI
Pasta: pokeapi_spark

Objetivo:
- Coletar e processar dados da PokeAPI.
- Estruturar dados para análise.
- Consolidar o fluxo de exploração e transformação com Spark.

Conteúdo principal:
- Notebook de análise e transformação.
- Dados brutos e tratados.
- README_POKEAPI.md com descrição do problema, execução e validação.

### 2. Desenvolvimento do Micro Serviço de Model Serving
Pasta: api_model_serving

Objetivo:
- Implementar uma API de serving para modelos de NLP.
- Expor endpoints para carga de modelo, inferência e consulta de registros.
- Disponibilizar estrutura para execução local, testes e containerização.

Conteúdo principal:
- Aplicação FastAPI.
- Módulos de gerenciamento de modelo.
- Schemas de entrada e saída.
- Dockerfile e testes básicos com pytest.
- README_API_MODEL_SERVING.md com descrição do problema, execução e testes.


