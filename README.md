# PicPay Case MLE

Este repositório reúne as entregas de dois problemas propostos no processo seletivo.

Importante:
- A pasta .Api_Model_Serving_v2 foi desconsiderada desta organização, por se tratar de uma proposta de evolução arquitetural para a API de Model Serving atual.

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

## Estrutura de alto nível

- api_model_serving: solução do problema de Micro Serviço de Model Serving
- pokeapi_spark: solução do problema de Análise de Dados com PokeAPI
- pyproject.toml, requirements.txt, uv.lock: configuração e dependências do projeto

## Leitura recomendada

Para executar ou entender cada entrega, consulte primeiro os READMEs das pastas:
- api_model_serving/README_API_MODEL_SERVING.md
- pokeapi_spark/README_POKEAPI.md
