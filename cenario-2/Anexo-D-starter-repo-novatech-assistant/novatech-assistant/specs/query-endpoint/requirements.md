# Requirements — Query Endpoint

## Objetivo

Disponibilizar um endpoint HTTP para consulta ao assistente da NovaTech utilizando arquitetura RAG baseada em Azure AI Search e Azure OpenAI.

## Requisitos Funcionais

- Receber requisições HTTP POST em `/api/query`.
- Validar o payload recebido.
- Gerar embedding da pergunta.
- Recuperar os cinco chunks mais relevantes.
- Montar o prompt respeitando o context budget definido na ADR-0002.
- Consultar o GPT-4o.
- Retornar resposta contendo o texto gerado e o `source_document`.

## Requisitos Não Funcionais

- Implementação em TypeScript.
- Azure Functions v4.
- Validação utilizando Zod.
- Logging estruturado com Pino.
- Retry com exponential backoff para chamadas Azure.