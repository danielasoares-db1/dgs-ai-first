### 1) Mapeamento necessidade -> server
| Necessidade | MCP Server | Tools | Resources | Prompts | Consumidores | Escopo mínimo | Justificativa |
|-------------|------------|-------|-----------|---------|--------------|---------------|---------------|
| Código, specs e skills | filesystem | Listar, ler, criar, editar e excluir arquivos | Arquivos do projeto | — | Desenvolvedores, Tech Lead, GitHub Copilot | `src/`, `specs/`, `skills/`, `prompts/` | Permite escrita apenas nos diretórios onde são produzidos artefatos do projeto. |
| Documentação de negócio | filesystem (read-only) | Listar e ler arquivos | Documentos da NovaTech | — | Desenvolvedores, QA, Product Specialist | `docs/novatech/` | A documentação é considerada fonte oficial e não deve ser alterada pelos agentes. |
| Corpus de recuperação (RAG) | filesystem (read-only) | Listar e ler arquivos | Chunks de referência | — | Desenvolvedores, QA | `data/retrieval-corpus/` | Os dados servem apenas como referência para recuperação de contexto e não devem sofrer alterações. |
| Histórico do repositório | git | status, log, diff, show, branch | Histórico Git | — | Desenvolvedores, Tech Lead | Repositório Git | Permite rastrear alterações e apoiar revisões de código sem modificar o histórico. |
| Memória persistente | memory | Criar, consultar e atualizar memória | Decisões do projeto e linguagem ubíqua | Prompts de memória | Toda a equipe | Namespace do projeto | Mantém decisões arquiteturais e terminologia compartilhada entre os agentes. |
| Descoberta de recursos MCP | everything | Listagem de tools, resources e prompts | Catálogo dos servidores disponíveis | Exemplos | Desenvolvedores | Sem acesso direto aos arquivos | Facilita a descoberta e depuração da configuração MCP. |

### 2) Arquivo `.mcp/mcp.json`
```json
{
	"servers": {
    "filesystem-code": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./src",
        "./specs",
        "./skills",
        "./prompts",
        "./tests"
      ],
      "type": "stdio"
    },

    "filesystem-docs": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./docs/novatech",
        "./docs/adr",
        "./docs/runbooks"
      ],
      "type": "stdio"
    },

    "filesystem-corpus": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./data/retrieval-corpus"
      ],
      "type": "stdio"
    }
  },
  "inputs": []
}
```

### Aplicação do princípio do Least Privilege

Cada servidor recebeu apenas o nível mínimo de acesso necessário para executar sua função. Os diretórios de documentação (`docs/novatech`) e do corpus (`data/retrieval-corpus`) são disponibilizados somente para leitura, enquanto apenas os diretórios destinados ao desenvolvimento recebem permissão de escrita. Essa abordagem reduz a superfície de ataque, evita alterações acidentais e protege documentos considerados fonte oficial do projeto.

### 3) Riscos e mitigação
- Risco 1: Escopo excessivo do Filesystem
  - impacto: Um servidor configurado para acessar toda a máquina pode expor arquivos sensíveis, como: .env, credenciais, chaves SSH
  - mitigação: Restringir o servidor aos diretórios estritamente necessários (src, specs, skills, prompts, docs e data), evitando acesso ao restante do sistema de arquivos.
- Risco 2: Alterações automáticas em arquivos
  - impacto: Um agente com permissão de escrita pode alterar código, documentação ou configurações sem revisão humana, introduzindo erros ou mudanças indevidas.
  - mitigação: Permitir escrita apenas nas pastas de desenvolvimento e adotar revisão humana antes de realizar commits ou merges.