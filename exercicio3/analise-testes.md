# Exercício 1.3 – Construção de Pipeline RAG com Ferramentas Open Source

## Análise dos Testes de Recuperação (Retrieval)

### Contexto

Foi implementado um pipeline de RAG utilizando:

* Python
* ChromaDB (vector store)
* Sentence Transformers (`all-MiniLM-L6-v2`)
* GitHub Copilot para auxílio na implementação

Os documentos do Anexo A foram ingeridos e indexados no ChromaDB utilizando chunking baseado em tamanho fixo de caracteres (700 caracteres com overlap de 120 caracteres).

Os testes abaixo foram realizados utilizando o script de busca semântica desenvolvido para o projeto e comparados com o mapa de cobertura fornecido no Anexo B.

---

# Teste 1 – Qual o prazo de devolução?

## Chunks esperados (Anexo B)

* POL-001-A
* POL-001-B

## Chunks recuperados

1. POL-001-politica-devolucao.md (custos de devolução)
2. POL-001-politica-devolucao.md (procedimento de devolução)
3. FAQ-atendimento.md

## Avaliação

❌ Incorreto

O pipeline não recuperou o trecho que contém explicitamente o prazo de devolução de 7 dias úteis. Os resultados retornados tratam de custos, reembolso e procedimento operacional.

## Observação

A principal informação solicitada pelo usuário não foi recuperada.

---

# Teste 2 – Posso devolver carga perigosa?

## Chunks esperados (Anexo B)

* POL-001-B
* FAQ-03

## Chunks recuperados

1. FAQ Item 32 – Carga perigosa com frete expresso
2. PROC-042 v1 – Frete para cargas perigosas
3. FAQ Item 22 – Seguro para cargas perigosas

## Avaliação

❌ Incorreto

O pipeline recuperou conteúdos relacionados a cargas perigosas, porém não relacionados à devolução.

O chunk principal esperado (POL-001-B), que informa que cargas perigosas não são elegíveis para devolução pelo processo padrão, não foi recuperado.

## Observação

A busca priorizou similaridade de termos ("carga perigosa") em vez da intenção completa da pergunta ("devolução de carga perigosa").

---

# Teste 3 – Qual o SLA do cliente Gold?

## Chunks esperados (Anexo B)

* SLA-2024-B
* SLA-2024-A

## Chunks recuperados

1. SLA-2024 – Medição e reportes
2. SLA-2024 – Classificação de clientes
3. FAQ Atendimento

## Avaliação

⚠️ Parcialmente correto

O pipeline identificou corretamente o documento SLA-2024, porém não recuperou diretamente a tabela de SLAs contendo os tempos de resposta e resolução.

## Observação

O documento correto foi encontrado, mas a seção mais relevante não apareceu entre os primeiros resultados.

---

# Teste 4 – Qual o multiplicador para o Sudeste?

## Chunks esperados (Anexo B)

* PROC-042v2-B

## Chunks recuperados

1. FAQ Item 8 – Frete especial
2. POL-001 – Custos de devolução
3. PROC-042-v2 – Multiplicadores regionais

## Avaliação

⚠️ Parcialmente correto

O chunk correto contendo o multiplicador atualizado para o Sudeste foi recuperado apenas na terceira posição.

O primeiro resultado foi um trecho do FAQ, considerado uma fonte informal.

## Observação

A informação correta foi encontrada, mas com baixa relevância no ranking.

---

# Teste 5 – O que acontece com carga danificada?

## Chunks esperados (Anexo B)

* FAQ-38

## Chunks recuperados

1. FAQ Item 38 – Carga danificada em trânsito
2. FAQ Item 27
3. FAQ Item 8

## Avaliação

✅ Correto

O chunk principal esperado foi recuperado em primeiro lugar.

## Observação

Neste caso o pipeline encontrou corretamente a informação necessária para responder à pergunta.

---

# Resumo dos Resultados

| Pergunta                             | Resultado   |
| ------------------------------------ | ----------- |
| Qual o prazo de devolução?           | ❌ Incorreto |
| Posso devolver carga perigosa?       | ❌ Incorreto |
| Qual o SLA do cliente Gold?          | ⚠️ Parcial  |
| Qual o multiplicador para o Sudeste? | ⚠️ Parcial  |
| O que acontece com carga danificada? | ✅ Correto   |

## Resultado geral

* Corretos: 1
* Parciais: 2
* Incorretos: 2

---

# Problemas Identificados

## Problema 1 – Chunking baseado apenas em tamanho

### Descrição

Os documentos foram divididos utilizando apenas uma janela de caracteres, sem considerar a estrutura semântica do Markdown.

### Impacto

Informações importantes ficaram separadas de seus títulos e contexto.

### Evidência

A pergunta sobre prazo de devolução não recuperou a seção 3.1 da POL-001.

### Correção proposta

Implementar chunking semântico baseado em títulos Markdown (`#`, `##`, `###`) preservando seções completas.

---

## Problema 2 – Ranqueamento inadequado

### Descrição

Chunks parcialmente relacionados apareceram acima de chunks mais relevantes.

### Impacto

O LLM pode receber contexto incorreto ou insuficiente para responder adequadamente.

### Evidência

A pergunta sobre multiplicador para o Sudeste retornou um FAQ antes do documento PROC-042-v2.

### Correção proposta

Implementar reranking dos resultados recuperados antes da montagem do prompt.

---

## Problema 3 – Priorização insuficiente de documentos oficiais

### Descrição

Documentos informais do FAQ aparecem frequentemente acima da documentação normativa.

### Impacto

Existe risco de respostas baseadas em informações não oficiais.

### Evidência

Perguntas sobre cargas perigosas retornaram FAQs em vez da política oficial POL-001.

### Correção proposta

Adicionar pesos ou regras de priorização documental:

* POL (alta prioridade)
* SLA (alta prioridade)
* PROC (alta prioridade)
* FAQ (baixa prioridade)

---

# Conclusão

O pipeline implementado demonstrou a viabilidade da arquitetura RAG utilizando ferramentas open source (Python, ChromaDB e Sentence Transformers), realizando corretamente a ingestão, geração de embeddings e busca semântica.

Entretanto, os testes evidenciaram limitações importantes relacionadas ao chunking e ao ranqueamento dos resultados recuperados. As melhorias propostas tendem a aumentar significativamente a precisão da recuperação e a qualidade das respostas geradas pelo LLM.

A prova de conceito foi considerada funcional para fins de validação técnica, mas requer ajustes antes de utilização em ambiente produtivo.
