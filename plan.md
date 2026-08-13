## Plan: Ingestao PokeAPI com Maturidade Tecnica

Objetivo: implementar a Etapa 1 com padrao de engenharia de dados confiavel e demonstrar maturidade tecnica no notebook, cobrindo concorrencia assincrona controlada, resiliencia de rede, governanca de erros, qualidade de dados e rastreabilidade operacional. A estrategia prioriza pipeline reproduzivel e auditavel, nao apenas velocidade.

## Steps
1. Definir criterios de aceite tecnicos da ingestao (completo, reproduzivel, observavel, tolerante a falhas), incluindo metas objetivas de qualidade e operacao.
2. Definir configuracao centralizada de runtime (BASE_URL, timeout, retries, backoff, concorrencia, tamanho de lote) e padrao de log estruturado por etapa.
3. Implementar cliente HTTP assincrono com politicas de resiliencia: timeout por request, retry com exponential backoff e jitter, classificacao de erros retryable vs nao-retryable, e circuit breaker simples por limite de falhas consecutivas.
4. Implementar extracao paginada deterministica do endpoint /pokemon usando next ate null, com protecao contra loop infinito e reconciliacao de contagem (count da API vs total coletado).
5. Implementar fan-out assincrono para detalhes por URL com semaforo de concorrencia, chunking por lotes e fail-safe por item (coleta continua mesmo com falhas isoladas).
6. Implementar normalizacao relacional com contrato de schema explicito para tabelas alvo (types, stats, abilities), garantindo chave de ligacao estavel por pokemon e integridade referencial basica.
7. Implementar camada de qualidade de dados com regras automatizadas: completude minima, unicidade de chave composta, dominios esperados e contagens por entidade. Gerar relatorio final de DQ no notebook.
8. Implementar persistencia intermediaria versionavel para reprodutibilidade local (raw JSON e tabelas normalizadas), habilitando reprocessamento sem novo consumo completo da API.
9. Materializar DataFrames Spark para as tabelas finais e validar leitura/consulta de sanidade para garantir prontidao da Etapa 3.
10. Documentar arquitetura e decisoes tecnicas no notebook: trade-offs de concorrencia, riscos de rate-limit, estrategia de retry, metricas de execucao e limites conhecidos.

## Relevant files
- /home/alexandre/Documents/picpay-case-mle/poke-spark/pokemon_spark.ipynb
- /home/alexandre/Documents/picpay-case-mle/README.md
- /home/alexandre/Documents/picpay-case-mle/pyproject.toml

## Verification
1. Executar smoke test com amostra pequena (10-20 pokemons) para validar conectividade, parser e schema alvo.
2. Executar carga completa e comparar count esperado da API com total de detalhes coletados, com relatorio de divergencias.
3. Medir metricas operacionais da ingestao: tempo total, throughput, taxa de falha, retries acionados e erros por classe HTTP.
4. Validar regras de qualidade: nulidade de campos criticos, duplicidade de chave composta e cardinalidade por pokemon nas tabelas de relacionamento.
5. Executar consultas Spark de sanidade nas tabelas finais para confirmar consistencia sem erros de parse ou tipos.
6. Reexecutar pipeline em modo cache (sem refetch total) para comprovar reprodutibilidade local e estabilidade dos resultados.

## Decisions
- Inclui: arquitetura de ingestao assincrona robusta, governanca de erros e controles de qualidade de dados.
- Exclui nesta etapa: analise de negocio, modelagem analitica avancada e otimizado de cluster Spark em producao.
- Fonte de verdade de chave pokemon: id do payload detalhado; URL usada apenas como fallback.
- Politica operacional: falha parcial controlada com rastreio completo, sem abortar pipeline na primeira excecao.

## Further Considerations
1. Biblioteca HTTP assincrona: opcao recomendada e httpx.AsyncClient por ergonomia e timeout granular; alternativa e aiohttp para alto volume.
2. Concorrencia inicial: iniciar em 8-10 e ajustar dinamicamente se ocorrerem respostas 429 ou aumento de latencia.
3. Qualidade de entrega: incluir secao de resultados com tabela de metricas antes de iniciar Etapa 2 para evidenciar maturidade tecnica.
