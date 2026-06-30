# Tasks — Query Endpoint

## Tarefa: QRY-001
- **Descrição:** Criar o endpoint HTTP `POST /api/query` utilizando Azure Functions v4, com validação do payload usando Zod.
- **Critérios de aceite:**
  - [ ] O endpoint aceita apenas requisições HTTP POST.
  - [ ] O campo `question` é obrigatório e deve ser uma string não vazia.
  - [ ] Requisições inválidas retornam HTTP 400 com mensagem de erro padronizada.
  - [ ] Requisições válidas retornam HTTP 202 indicando que a consulta foi aceita.
- **Dependências:** Nenhuma.
- **Estimativa:** P

---

## Tarefa: QRY-002
- **Descrição:** Implementar o cliente de geração de embeddings utilizando Azure OpenAI.
- **Critérios de aceite:**
  - [ ] O endpoint gera um embedding para uma pergunta válida.
  - [ ] Chamadas ao Azure utilizam retry com exponential backoff.
  - [ ] Erros são tratados sem expor informações sensíveis.
- **Dependências:** QRY-001.
- **Estimativa:** M

---

## Tarefa: QRY-003
- **Descrição:** Integrar o endpoint ao Azure AI Search para recuperar os cinco chunks mais relevantes.
- **Critérios de aceite:**
  - [ ] São retornados no máximo cinco chunks.
  - [ ] Cada resultado contém os metadados do documento de origem.
  - [ ] Documentos contraditórios respeitam a regra de vigência definida na ADR-0003.
- **Dependências:** QRY-001, QRY-002.
- **Estimativa:** M

---

## Tarefa: QRY-004
- **Descrição:** Montar o prompt final utilizando o system prompt, os chunks recuperados e a pergunta do usuário.
- **Critérios de aceite:**
  - [ ] O system prompt é carregado de `/prompts/system-prompt.md`.
  - [ ] O contexto respeita o orçamento definido na ADR-0002.
  - [ ] O histórico da conversa é limitado a três interações.
- **Dependências:** QRY-003.
- **Estimativa:** M

---

## Tarefa: QRY-005
- **Descrição:** Enviar o prompt ao modelo GPT-4o e retornar a resposta ao cliente.
- **Critérios de aceite:**
  - [ ] A resposta contém o texto gerado pelo modelo.
  - [ ] A resposta inclui o campo `source_document`.
  - [ ] Erros do modelo são tratados de forma controlada.
- **Dependências:** QRY-004.
- **Estimativa:** M

---

## Tarefa: QRY-006
- **Descrição:** Implementar logging estruturado e testes iniciais do fluxo de consulta.
- **Critérios de aceite:**
  - [ ] O endpoint registra logs utilizando Pino.
  - [ ] Existe teste para requisição válida.
  - [ ] Existe teste para payload inválido.
  - [ ] Existe teste para cenário sem resultados de busca.
- **Dependências:** QRY-001, QRY-005.
- **Estimativa:** M