# Análise de Dados com PokeAPI (Spark)

## Descrição do problema

Este diretório contém a solução do problema de análise de dados com PokeAPI.

Objetivos principais:
- extrair dados da PokeAPI
- organizar os dados em camadas (raw/trusted)
- aplicar transformações e análises com Spark
- registrar o processo em notebook reproduzível

## Estrutura principal

- pokemon_spark.ipynb: notebook com extração, transformação e análises
- data/raw: dados brutos coletados da API
- data/trusted: área para dados transformados/consolidados

## Pré-requisitos

- Python 3.14+
- Dependências do projeto instaladas
- Ambiente com Jupyter Notebook/Lab

## Execução passo a passo

1. Vá para a raiz do repositório:

```bash
cd picpay-case-mle
```

2. Instale dependências (caso ainda não tenha feito):

```bash
uv sync
```

3. Abra o notebook:

```bash
jupyter notebook pokeapi_spark/pokemon_spark.ipynb
```

4. Execute todas as células na ordem (Restart Kernel + Run All).

## Teste/validação da solução

Após a execução completa do notebook, valide:

1. Arquivos da camada raw existem:

```bash
ls -la pokeapi_spark/data/raw
```

Esperado conter pelo menos:
- pokemon_urls_list.json
- pokemons_raw_data.json

2. Verificação rápida de conteúdo JSON:

```bash
python -c "import json; print(len(json.load(open('pokeapi_spark/data/raw/pokemon_urls_list.json'))))"
```

3. Se o notebook gerar saídas trusted, confirme os artefatos:

```bash
ls -la pokeapi_spark/data/trusted
```

## Critério de sucesso

- notebook executa sem erro
- arquivos raw são gerados/lidos corretamente
- análises Spark são concluídas e resultados ficam visíveis no notebook