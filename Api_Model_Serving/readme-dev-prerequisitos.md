# Desenvolvimento do Micro Serviço de Model Serving

## Objetivo
O PicPay possui um serviço de PIX por WhatsApp onde o cliente envia um texto ou áudio para o
assistente de pagamentos do PicPay no WhatsApp solicitando uma operação bancária da seguinte
forma:
Faça um PIX de R$10,00 para o João amanhã
O assistente então interpreta essa mensagem e realiza a operação financeira solicitada.
O objetivo dessa etapa é construir um micro serviço que receba uma mensagem desse tipo e retorne
os dados que serão utilizados para dar continuidade na trasação, ex:
- OPERACAO: PIX
- VALOR: 10,00
- DESTINO: João
- DATA: amanhã

O serviço deve ser construído em Python, containerizado utilizando Docker e executável localmente.


## Requisitos mínimos da API
O micro serviço deve conter, no mínimo, os seguintes endpoints:

#### POST /load/
Registra uma nova versão do modelo.
- Payload:
    - model: str - Nome do modelo spaCy a ser utilizado, ex: en_core_web_sm, en_core_web_md, en_core_web_lg
- Função: Ao passar o nome do modelo spaCy o ms deverá ver se ja tem esse modelo baixado,
caso contrário baixar o modelo e deixar a disposição,
- Dica: Ex de download python3 -m spacy download en_core_web_sm
---

#### POST /predict/
Realiza inferência utilizando o modelo ativo ou uma versão específica.
- Payload:
    - text: str - Texto (em ingles) a ser analisado
    - model: str - Nome do modelo spaCy a ser utilizado, ex: en_core_web_sm,
en_core_web_md, en_core_web_lg
- Função: Carrega o modelo solicitado e realiza inferência utilizando o modelo passado como
  parâmetro
- Exemplo de Entrada: Can you send $45 to Michael on June 3?
- Exemplo de Saída:
    - MONEY : 45
    - PERSON : Michael
    - DATE : June 3
- Dica: Ex de load do modelo: spacy.load("en_core_web_sm")
---
#### GET /list/
Lista as predições realizadas.
- Deve retornar histórico de:
    - Input recebido
    - Output gerado
    - Timestamp
    - Versão do modelo utilizada
---
#### Endpoints adicionais (sugeridos)
O candidato pode propor e implementar outros endpoints que considere relevantes. Exemplos:
- GET /models/ → lista versões disponíveis
- GET /health/ → healthcheck do serviço
- DELETE /models/{version} → remove versão

### Requisitos técnicos
- Linguagem: Python
- Framework sugerido: FastAPI, Flask ou similar
- Conteinerização obrigatória com Docker
- Serviço deve rodar localmente

### Boas práticas esperadas
- Organização de código (estrutura de projeto)
- Separação de responsabilidades
- Tratamento de erros
- Logs estruturados
- Versionamento claro
- README explicando como rodar