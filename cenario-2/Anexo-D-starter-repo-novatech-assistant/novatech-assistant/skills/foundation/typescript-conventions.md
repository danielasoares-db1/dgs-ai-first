# TypeScript Conventions

## Contexto
O NovaTech Assistant é um projeto TypeScript com Azure Functions v4, integração com Azure OpenAI e Azure AI Search, testes com Vitest e consumo por agentes de IA como GitHub Copilot e Claude. Neste repositório, a maior fonte de inconsistência não é a linguagem em si, mas a variação de estilo, contratos e decisões triviais tomadas de forma manual por diferentes autores.

Esta skill existe para padronizar a escrita de TypeScript em todo o projeto. Ela deve ser usada sempre que o código for criado ou alterado por IA ou por pessoas que precisem seguir o mesmo contrato estrutural.

## Objetivo
Garantir que o TypeScript gerado no NovaTech Assistant seja:

- consistente entre módulos;
- previsível para leitura, revisão e teste;
- compatível com `strict: true`;
- fácil de validar com Vitest e de operar em Azure Functions;
- seguro para manutenção por Tech Lead, Dev Sênior, Dev Pleno, QA, GitHub Copilot e Claude.

## Quando utilizar
Use esta skill sempre que estiver:

- criando ou revisando código TypeScript;
- adicionando handlers de Azure Functions;
- definindo tipos, interfaces, schemas ou modelos de domínio;
- escrevendo serviços, helpers, builders, adapters ou validators;
- implementando integração com Azure OpenAI, Azure AI Search ou React;
- criando ou ajustando testes em Vitest;
- gerando código assistido por IA para qualquer módulo do NovaTech Assistant.

## Regras obrigatórias (DEVE)

- DEVE usar TypeScript com tipagem explícita sempre que a inferência não deixar o contrato evidente.
- DEVE manter `strict: true` como pressuposto e evitar qualquer solução que dependa de tipagem frouxa.
- DEVE declarar tipos de entrada e saída para funções públicas, handlers e helpers reutilizáveis.
- DEVE preferir `type` para dados compostos simples e `interface` apenas quando houver necessidade clara de extensão ou contrato aberto.
- DEVE nomear funções, variáveis e tipos de forma semântica e orientada ao domínio.
- DEVE manter módulos pequenos e com responsabilidade única.
- DEVE extrair lógica de validação, transformação e montagem de resposta para funções auxiliares quando o handler começar a ficar verboso.
- DEVE usar `async` e `await` de forma direta, evitando encadeamentos desnecessários de `then`.
- DEVE tratar explicitamente casos de erro, retorno vazio e estados de falha de dependências externas.
- DEVE validar entradas com Zod quando o código receber payload externo, parâmetros HTTP ou dados de origem não confiável.
- DEVE retornar objetos com contratos estáveis e serializáveis em endpoints e serviços expostos.
- DEVE evitar constantes mágicas espalhadas; quando um valor tiver significado de negócio ou operação, mova-o para uma constante nomeada.
- DEVE importar apenas o que é usado.
- DEVE preferir caminhos relativos curtos e organização por domínio ou responsabilidade.
- DEVE escrever testes para qualquer lógica não trivial, especialmente transformações, validações, montagem de prompt e mapeamento de respostas.
- DEVE manter compatibilidade com o estilo do projeto e com as skills Foundation e Domain relacionadas.

## Regras proibidas (NÃO DEVE)

- NÃO DEVE usar `any` como solução padrão.
- NÃO DEVE usar `as` para esconder problema de tipagem quando uma modelagem correta resolveria o caso.
- NÃO DEVE duplicar contratos de entrada e saída em múltiplos arquivos sem necessidade.
- NÃO DEVE misturar regra de negócio com detalhes de transporte HTTP ou implementação de infraestrutura.
- NÃO DEVE criar funções longas que façam validação, transformação, chamada externa e resposta final no mesmo bloco sem separação.
- NÃO DEVE depender de variáveis globais mutáveis para manter estado de execução.
- NÃO DEVE usar nomes genéricos como `data`, `result`, `value` ou `handler` quando o contexto permitir um nome mais específico.
- NÃO DEVE introduzir abstrações antecipadas sem repetição real.
- NÃO DEVE espalhar literals de status, mensagens de erro ou nomes de campos de forma inconsistente.
- NÃO DEVE suprimir erros silenciosamente.
- NÃO DEVE acoplar testes a detalhes internos desnecessários se o comportamento observável já for suficiente.

## Exemplos DO e DON'T

### DO

```ts
type QueryRequest = {
  question: string;
};

type QueryResponse = {
  answer: string;
  sourceDocument: string | null;
};

export async function handleQuery(request: QueryRequest): Promise<QueryResponse> {
  const normalizedQuestion = request.question.trim();

  return {
    answer: normalizedQuestion,
    sourceDocument: null,
  };
}
```

### DON'T

```ts
export async function handleQuery(request: any) {
  const answer = request.question.trim();
  return {
    answer,
    source_document: null,
    extra: undefined,
  };
}
```

### DO

```ts
import { z } from "zod";

const feedbackSchema = z.object({
  questionId: z.string().min(1),
  rating: z.number().int().min(1).max(5),
});

type FeedbackPayload = z.infer<typeof feedbackSchema>;

export function parseFeedbackPayload(input: unknown): FeedbackPayload {
  return feedbackSchema.parse(input);
}
```

### DON'T

```ts
export function parseFeedbackPayload(input: any) {
  if (!input.questionId) {
    throw new Error("invalid payload");
  }

  return input;
}
```

### DO

```ts
type SearchChunk = {
  id: string;
  content: string;
  score: number;
};

export function selectTopChunks(chunks: SearchChunk[]): SearchChunk[] {
  return [...chunks].sort((left, right) => right.score - left.score).slice(0, 5);
}
```

### DON'T

```ts
export function selectTopChunks(chunks) {
  chunks.sort((a, b) => b.score - a.score);
  return chunks.slice(0, 5);
}
```

## Anti-padrões comuns gerados por IA

- uso excessivo de `any`, `unknown` sem refinamento ou casts apressados;
- handlers que fazem tudo sozinhos e escondem a lógica em blocos longos;
- nomes genéricos que perdem o contexto do domínio;
- mistura de camelCase, snake_case e variações de contrato dentro do mesmo módulo;
- retorno de estruturas instáveis ou inconsistentes entre funções parecidas;
- schemas Zod incompletos, duplicados ou com mensagens de erro inconsistentes;
- funções utilitárias criadas sem necessidade real de reutilização;
- testes frágeis que validam implementação em vez de comportamento;
- importações desnecessárias ou comentários que apenas repetem o código.

## Dependências de outras skills

- `project-structure`: para saber onde o código TypeScript deve viver no repositório.
- `error-handling`: para padronizar exceções, respostas e cenários de falha.
- `spec-driven-development`: para alinhar o código ao requisito, plano e tasks da spec.
- `azure-functions-endpoint`: para aplicar estas convenções em handlers HTTP.
- `testing-patterns`: para escrever testes coerentes com as mesmas convenções.
- `react-components`: para manter consistência também no front-end quando o código TypeScript for usado em componentes.
