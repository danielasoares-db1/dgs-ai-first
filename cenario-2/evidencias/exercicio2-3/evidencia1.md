## Exercício 2.3 — Estratégia de skills do projeto

### 1) Árvore de skills
```text
skills/
	foundation/
		typescript-conventions.md
		project-structure.md
		error-handling.md
		spec-driven-development.md
	domain/
		azure-functions-endpoint.md
		azure-ai-search-integration.md
		react-components.md
		testing-patterns.md
	artifact/
		create-rag-endpoint.md
		create-integration-test.md
		create-react-card.md
```

### 2) Mapeamento de criação/consumo
| Nome da skill | Nível | Frase de ativação | Quem cria | Quem mantém | Quem consome | Frequência estimada de uso |
|---|---|---|---|---|---|---|
| `typescript-conventions` | Foundation | "Siga as convenções TypeScript do NovaTech" | Tech Lead | Tech Lead + Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Alta |
| `project-structure` | Foundation | "Organize o código conforme a estrutura do repositório NovaTech" | Tech Lead | Tech Lead | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Alta |
| `error-handling` | Foundation | "Aplique o padrão de erros do NovaTech" | Tech Lead | Tech Lead + Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior, QA | Alta |
| `spec-driven-development` | Foundation | "Escreva a spec no formato SDD do NovaTech" | Product Specialist + Tech Lead | Product Specialist + Tech Lead | GitHub Copilot, Claude, Product Specialist, Tech Lead, Dev Sênior | Alta |
| `azure-functions-endpoint` | Domain | "Crie um endpoint Azure Functions v4 no padrão NovaTech" | Tech Lead | Tech Lead + Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Alta |
| `azure-ai-search-integration` | Domain | "Integre com Azure AI Search no padrão NovaTech" | Tech Lead + Dev Sênior | Dev Sênior | GitHub Copilot, Claude, Dev Sênior | Média |
| `react-components` | Domain | "Crie componente React no padrão NovaTech" | Dev Sênior | Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Média |
| `testing-patterns` | Domain | "Escreva teste Vitest no padrão NovaTech" | QA + Dev Sênior | QA + Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior, QA | Alta |
| `create-rag-endpoint` | Artifact | "Implemente o endpoint RAG do NovaTech" | Tech Lead + Dev Sênior | Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Média |
| `create-integration-test` | Artifact | "Crie um teste de integração para este fluxo" | QA + Dev Sênior | QA | GitHub Copilot, Claude, Dev Pleno, Dev Sênior, QA | Alta |
| `create-react-card` | Artifact | "Crie um card React/Adaptive Card para este caso" | Dev Sênior | Dev Sênior | GitHub Copilot, Claude, Dev Pleno, Dev Sênior | Média |

### 3) SKILL.md Foundation escolhida
- Skill escolhida: `typescript-conventions`
- Caminho do arquivo: `skills/foundation/typescript-conventions.md`
- Conteúdo final:

	A skill define as convenções obrigatórias de TypeScript para o NovaTech Assistant. Ela cobre contexto, objetivo, quando utilizar, regras DEVE/NÃO DEVE, exemplos DO e DON'T, anti-padrões comuns gerados por IA e dependências de outras skills.

	Principais regras:
	- usar tipagem explícita quando a inferência não for suficiente;
	- manter `strict: true` como pressuposto;
	- declarar tipos de entrada e saída em funções públicas, handlers e helpers;
	- validar payloads externos com Zod;
	- evitar `any`, casts apressados e funções longas que misturam responsabilidades;
	- escrever código pequeno, semântico e testável;
	- manter o contrato estável para consumo por GitHub Copilot e Claude.

### 4) Evidência de uso com Copilot
- Prompt usado: "Utilize uma skill skills/foundation/typescript-conventions.md como referência para gerar um endpoint simples em TypeScript. Ao final, informe quais regras da skill foram seguidas, quais regras não puderam ser aplicadas e quais melhorias você sugere para tornar a skill mais útil para futuras gerações de código."
- O que o Copilot seguiu: criou um endpoint simples de health em TypeScript com `app.http`, tipagem explícita da resposta, `async/await`, `logger` estruturado, contrato de retorno estável, nomes semânticos e sem uso de `any`.
- O que ignorou: não aplicou Zod porque o endpoint não recebe payload; também não extraiu helpers auxiliares porque o caso era propositalmente mínimo e legível inline.
- Ajustes propostos na skill: incluir um template específico para endpoints simples como health check; explicitar quando usar helper/builder versus resposta inline; adicionar exemplos de handlers `GET` e `POST`; e documentar um mini-contrato de resposta para endpoints pequenos.