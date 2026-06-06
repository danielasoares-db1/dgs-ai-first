## Interação 1 - Análise das fontes

### Prompt enviado ao Copilot

Leia o arquivo anexo-a-documentacao-simulada-novatech.md e faça um resumo executivo do cenário da NovaTech.

Identifique:
- objetivo do assistente
- fontes de informação disponíveis
- principais desafios técnicos
- principais requisitos de negócio

Apenas resuma o cenário.

### Resumo da resposta

Vou ler o arquivo completo para sintetizar um resumo executivo fiel ao cenário da NovaTech, cobrindo exatamente os quatro pontos que você pediu. Em seguida te entrego só o resumo, sem propor solução técnica adicional.

Resumo Executivo do Cenário NovaTech

Objetivo do assistente
O assistente deve apoiar atendimento e operações com respostas confiáveis, rastreáveis e alinhadas à documentação oficial da NovaTech, tratando ambiguidades de forma explícita. Na prática, ele precisa responder perguntas operacionais (devolução, frete especial, SLA, exceções) com base em evidência documental, reduzindo risco de orientação incorreta ao cliente.

Fontes de informação disponíveis
A base combina cinco documentos com pesos diferentes:

Política normativa de devolução (POL-001), com regras obrigatórias e exceções.
Procedimento de frete especial em duas versões (PROC-042 v1 e PROC-042-v2), com coexistência e conflito de parâmetros.
Tabela contratual de SLA por tier de cliente (SLA-2024), com compromissos formais.
FAQ de atendimento (informal), útil como conhecimento prático, mas sem validação formal.
Notas de meta-contexto que já apontam contradições e lacunas na base.
Principais desafios técnicos

Resolver conflitos entre versões (v1 vs v2) sem perder consistência da resposta.
Priorizar hierarquia de fontes (normativo/contratual acima do FAQ informal).
Tratar regras condicionais e temporais (transição de vigência, exceções por tipo de carga, tier de cliente).
Garantir recuperação precisa em RAG (chunking, contexto suficiente e citação correta da fonte).
Lidar com lacunas documentais sem “inventar” política, sinalizando ausência de base formal quando necessário.
Principais requisitos de negócio

Conformidade: respostas devem seguir documentos oficiais e reduzir risco regulatório/operacional.
Precisão operacional: aplicar corretamente prazos, elegibilidade e fluxos de devolução.
Consistência comercial: calcular/explicar frete especial conforme versão aplicável e regras de transição.
Cumprimento contratual: respeitar SLAs por tier (Gold, Silver, Standard), incluindo incidentes críticos e penalidades.
Governança do atendimento: quando houver conflito ou ausência de norma, escalar para áreas responsáveis (Comercial, Gestão de Riscos, Compliance/Jurídico) em vez de assumir regras não documentadas.

Com base no cenário da NovaTech e nas informações abaixo:

- PDFs com tabelas complexas
- PDFs escaneados
- Wiki com links internos
- Planilhas com fórmulas

Explique os desafios para um pipeline de RAG.

Para cada tipo de documento descreva:
1. Desafio técnico
2. Impacto na qualidade das respostas
3. Estratégia de tratamento

Escreva em formato de documento técnico.

Documento Técnico: Desafios de Pipeline RAG para Heterogeneidade Documental no Cenário NovaTech

1. Objetivo
Este documento descreve os principais desafios de engenharia de um pipeline de RAG quando a base de conhecimento combina quatro tipos de fonte: PDFs com tabelas complexas, PDFs escaneados, wiki com links internos e planilhas com fórmulas.
Para cada tipo, são apresentados:

desafio técnico,
impacto na qualidade das respostas,
estratégia recomendada de tratamento.
2. Contexto do Problema
No cenário NovaTech, a qualidade da resposta depende de:

recuperar o trecho correto da fonte correta,
preservar estrutura semântica (regras, exceções, vigência, fórmulas e contexto),
reduzir ambiguidades e conflitos entre documentos.
Quando o pipeline não preserva estrutura e contexto, o modelo tende a responder com confiança alta, mas precisão baixa.
3. Desafios por Tipo de Documento

3.1 PDFs com tabelas complexas
1. Desafio técnico

Extração linear do texto quebra relações de linha e coluna.
Cabeçalhos multinível, células mescladas e notas de rodapé perdem vínculo semântico.
Layouts com várias colunas geram ordem de leitura incorreta.
Tabelas podem conter regras críticas (SLA, multiplicadores, limites) difíceis de reconstruir.
2. Impacto na qualidade das respostas

Respostas com valores trocados entre categorias.
Erros de regra condicional por perda de contexto tabular.
Citações corretas de documento, porém com interpretação numérica errada.
Aumento de alucinação quando a tabela não é convertida em estrutura consultável.
3. Estratégia de tratamento

Usar parser orientado a tabela, não apenas extração de texto bruto.
Converter tabelas para estrutura canônica (JSON tabular ou Markdown estruturado com metadados).
Persistir metadados por célula: documento, página, linha, coluna, cabeçalho pai.
Criar chunks semânticos por bloco de tabela (não por token fixo), preservando cabeçalhos.
Aplicar validação automática pós-extração com regras de consistência.
Na resposta, forçar grounding em células específicas e incluir referência de origem.
3.2 PDFs escaneados
1. Desafio técnico

Conteúdo é imagem, exigindo OCR.
OCR pode falhar em baixa resolução, ruído, carimbos, rotação e tipografia degradada.
Perda de acentuação e números críticos.
Segmentação de blocos (título, corpo, tabela, rodapé) costuma ser imprecisa.
2. Impacto na qualidade das respostas

Recuperação incompleta ou com termos distorcidos.
Queda de recall: o trecho correto não é encontrado.
Erros em datas, prazos e percentuais por leitura incorreta.
Respostas inconsistentes entre documentos digitalizados e nativos.
3. Estratégia de tratamento

Implementar pré-processamento de imagem: deskew, denoise, binarização e aumento de contraste.
Adotar OCR com suporte a português e fallback multimotor.
Calcular confiança por bloco e marcar trechos de baixa confiabilidade.
Reprocessar automaticamente páginas com baixa qualidade de OCR.
Armazenar texto OCR junto com bounding boxes para rastreabilidade.
Incluir etapa de revisão humana para documentos críticos.
Priorizar documentos nativos quando houver duplicidade entre fonte escaneada e fonte textual.
3.3 Wiki com links internos
1. Desafio técnico

Conteúdo distribuído em múltiplas páginas interdependentes.
Links internos carregam semântica de navegação e hierarquia.
Conteúdo dinâmico e edições frequentes geram drift de embeddings.
Risco de indexação parcial (página sem anexos, anexos sem página, páginas órfãs).
2. Impacto na qualidade das respostas

Respostas sem contexto completo, ignorando pré-requisitos ou exceções.
Contradições por recuperar versão antiga ou página fora da hierarquia.
Perda de explicabilidade quando a resposta não reflete cadeia de evidências.
Maior chance de selecionar trechos isolados sem o contexto de decisão.
3. Estratégia de tratamento

Fazer crawling com preservação de grafo de links.
Indexar conteúdo com metadados de navegação: página pai, seção, backlinks e versão.
Usar recuperação híbrida: lexical, vetorial e expansão por vizinhança no grafo.
Aplicar chunking por seção lógica, mantendo títulos e breadcrumbs.
Rodar ingestão incremental com controle de versões e invalidar embeddings antigos.
Em consultas críticas, recuperar página-alvo mais páginas relacionadas por link semântico.
3.4 Planilhas com fórmulas
1. Desafio técnico

Conhecimento está no valor e na fórmula.
Dependências entre abas e referências cruzadas dificultam interpretação linear.
Fórmulas podem incorporar regras de negócio implícitas.
Valores mudam com parâmetros temporais, cenários e filtros.
Risco de ingerir apenas valor estático e perder lógica de cálculo.
2. Impacto na qualidade das respostas

Respostas numericamente corretas em um contexto, mas erradas em outro.
Incapacidade de explicar como o resultado foi calculado.
Erros de decisão quando regras condicionais da fórmula não são capturadas.
Falta de auditoria e baixa confiança em respostas que envolvem cálculo.
3. Estratégia de tratamento

Extrair estrutura completa da planilha: abas, células, fórmulas, intervalos nomeados e dependências.
Construir representação dual:
camada de dados (valores),
camada lógica (fórmulas e regras).
Materializar regras em linguagem intermediária interpretável.
Versionar snapshots e registrar data de referência dos valores.
Para perguntas de cálculo, usar abordagem tool-augmented:
recuperar regra,
executar cálculo com parâmetros atuais,
devolver resultado com trilha de auditoria.
Validar automaticamente resultados com testes de regressão numérica.
4. Recomendações Arquiteturais Transversais

Pipeline multimodal de ingestão, com ramificações por tipo documental.
Esquema de metadados unificado: fonte, versão, vigência, confiança de extração, seção e evidência.
Estratégia de chunking específica por formato, evitando abordagem única.
Recuperação híbrida com reranking por criticidade de domínio.
Camada de governança para conflitos documentais: prioridade de fonte e política de desempate.
Observabilidade de ponta a ponta:
qualidade de parsing,
cobertura de indexação,
precisão de recuperação,
groundedness da resposta.
Human-in-the-loop para casos com baixa confiança, conflito de fontes ou lacuna documental.
5. Conclusão
No cenário NovaTech, o maior risco para RAG não é apenas buscar informação, mas preservar estrutura e contexto normativo em fontes heterogêneas.
A combinação de ingestão especializada por formato, metadados ricos, recuperação híbrida e governança de conflito é o caminho mais efetivo para elevar precisão, explicabilidade e confiabilidade operacional das respostas.

## Interação 2 - Estimativa de tokens

### Prompt enviado

Com base no exercício da NovaTech:

- 800 PDFs
- média de 10 páginas por PDF
- média de 500 palavras por página

- 400 páginas wiki
- média de 1500 palavras por página

Utilize a regra prática de 0,75 palavras por token.

Calcule a estimativa do tamanho total da base em tokens.

Apresente os cálculos passo a passo e escreva em formato de documento técnico.

### Resultado

Documento Técnico: Estimativa de Tamanho da Base em Tokens (NovaTech)

1. Objetivo
Estimar o tamanho total da base documental em tokens usando a regra prática informada:
1 token ≈ 0,75 palavra.

2. Dados de Entrada

PDFs:
Quantidade de arquivos: 800
Média de páginas por PDF: 10
Média de palavras por página: 500
Wiki:
Quantidade de páginas: 400
Média de palavras por página: 1500
3. Regra de Conversão
Para converter palavras em tokens:

[
\text{tokens} = \frac{\text{palavras}}{0,75}
]

4. Cálculo dos PDFs

Palavras por PDF:
[
10 \times 500 = 5.000 \text{ palavras/PDF}
]

Palavras totais em PDFs:
[
800 \times 5.000 = 4.000.000 \text{ palavras}
]

Tokens estimados para PDFs:
[
\frac{4.000.000}{0,75} = 5.333.333{,}33 \text{ tokens}
]

5. Cálculo da Wiki

Palavras totais na wiki:
[
400 \times 1.500 = 600.000 \text{ palavras}
]

Tokens estimados para wiki:
[
\frac{600.000}{0,75} = 800.000 \text{ tokens}
]

6. Cálculo Total da Base

Palavras totais:
[
4.000.000 + 600.000 = 4.600.000 \text{ palavras}
]

Tokens totais estimados:
[
\frac{4.600.000}{0,75} = 6.133.333{,}33 \text{ tokens}
]

Resultado final estimado: 6.133.333 tokens (aprox. 6,13 milhões de tokens).

7. Observação Técnica
Essa é uma estimativa macro. O total real pode variar conforme idioma, formatação, tabelas, números, siglas e qualidade de extração de texto (especialmente em PDFs).

## Interação 3 - Orçamento de contexto

### Prompt enviado

Com base no exercício da NovaTech:

- GPT-4o com janela de contexto de 128.000 tokens
- 2.000 tokens reservados para system prompt e instruções
- chunks de aproximadamente 500 tokens

Elabore uma análise técnica de orçamento de contexto.

Inclua:
1. Quantos chunks cabem teoricamente na janela.
2. Por que não é recomendável utilizar toda a capacidade disponível.
3. O conceito de "lost in the middle".
4. Como isso influencia a estratégia de retrieval em um sistema RAG.

Escreva em formato de documento técnico.

### Resultado

Documento Técnico: Análise de Orçamento de Contexto para RAG (Cenário NovaTech)

1. Premissas

Modelo com janela de contexto: 128.000 tokens.
Reserva fixa para system prompt e instruções: 2.000 tokens.
Tamanho médio de chunk: 500 tokens.
2. Capacidade Teórica de Chunks

Contexto útil para recuperação:
[
128.000 - 2.000 = 126.000 \text{ tokens}
]
Número teórico de chunks:
[
\frac{126.000}{500} = 252 \text{ chunks}
]
Resultado teórico: cabem até 252 chunks de 500 tokens.

3. Por que não usar 100% da janela
Mesmo com capacidade teórica de 252 chunks, não é recomendável preencher toda a janela por quatro motivos principais:

É necessário reservar espaço para a pergunta do usuário e para a geração da resposta.
Quanto mais contexto irrelevante, maior a chance de ruído semântico e menor precisão factual.
Mais tokens elevam custo e latência sem ganho proporcional de qualidade.
O modelo não “lê tudo com o mesmo peso”; excesso de contexto pode reduzir a eficácia de atenção sobre evidências críticas.
Prática recomendada: trabalhar com orçamento operacional abaixo do máximo teórico, mantendo margem para prompt dinâmico, reescrita de consulta e resposta final.

4. Conceito de Lost in the Middle
Lost in the middle é o efeito em que informações posicionadas no meio de um contexto muito longo tendem a ser menos utilizadas pelo modelo do que conteúdos no início e no fim.
Em termos práticos, dois trechos igualmente relevantes podem ter impacto diferente na resposta apenas por posição no prompt.

Consequência: ampliar contexto indiscriminadamente pode piorar a recuperação efetiva de evidência, mesmo sem ultrapassar o limite de tokens.

5. Impacto na Estratégia de Retrieval em RAG
Esse fenômeno altera diretamente o desenho de retrieval:

Priorizar qualidade de ranking sobre quantidade de chunks.
Manter top-k enxuto e calibrado por tipo de pergunta.
Reordenar contexto para colocar evidências mais fortes em posições de maior atenção.
Aplicar deduplicação e compressão contextual antes da montagem do prompt.
Usar recuperação em múltiplos estágios:
[
\text{recall alto inicial} \rightarrow \text{reranking} \rightarrow \text{contexto final enxuto}
]
Favorecer chunks semanticamente completos (com metadados de seção, versão e vigência), em vez de blocos longos pouco específicos.
Em casos de conflito documental (como versões PROC-042), trazer menos chunks, porém mais autoritativos e explicitamente contrastados.
6. Conclusão
A capacidade teórica é de 252 chunks, mas o orçamento efetivo deve ser menor para preservar precisão, custo, latência e robustez. Em RAG, desempenho não depende de “colocar tudo no contexto”, e sim de selecionar, ordenar e comprimir evidências com alta relevância, mitigando o efeito de lost in the middle.

## Interação 4 - Estratégia de chunking

### Prompt enviado

Com base no cenário da NovaTech, proponha uma estratégia de chunking para:

- PDFs textuais
- PDFs com tabelas
- Wiki com links internos
- Planilhas com fórmulas

A análise deve explicar:

1. Como os documentos serão divididos em chunks.
2. Tamanho recomendado dos chunks.
3. Quando utilizar overlap.
4. Como a estratégia atende ao tipo de pergunta esperado dos usuários.
5. Como a estratégia reduz os efeitos de lost in the middle.

Escreva em formato de documento técnico.

### Resultado

Documento Técnico: Estratégia de Chunking para RAG no Cenário NovaTech

1. Objetivo
Definir uma estratégia de chunking por tipo de fonte para melhorar recuperação, precisão de resposta e robustez contra lost in the middle em perguntas típicas de atendimento, operações e comercial.

2. Perguntas esperadas no cenário NovaTech

Regras normativas: prazo de devolução, exceções, critérios de elegibilidade.
Cálculo e vigência: multiplicadores, fator de peso, diferenças entre versões de procedimento.
SLA contratual: tempos por tier, incidentes críticos, penalidades.
Operação prática: quando escalar para Riscos, Comercial ou Compliance.
Perguntas comparativas: “qual regra vale neste caso?” com conflito documental.
3. Estratégia por tipo de documento

3.1 PDFs textuais
Divisão em chunks
Dividir por estrutura semântica do documento: título, seção e subseção. Evitar corte no meio de listas de regras, exceções e prazos. Cada chunk deve preservar contexto mínimo de decisão (regra + condição + exceção).

Tamanho recomendado
Entre 350 e 550 tokens por chunk. Faixa ideal operacional: 450 tokens.

Quando usar overlap
Usar overlap de 10% a 15% apenas entre subseções contíguas quando houver continuidade lógica forte (exemplo: regra geral seguida de exceção). Não usar overlap alto em listas independentes.

Aderência às perguntas dos usuários
Esse formato favorece perguntas objetivas de política e procedimento, porque o chunk já chega “pronto para decisão”, reduzindo a necessidade de montar contexto de múltiplos blocos.

Redução de lost in the middle
Chunks menores e semanticamente completos permitem top-k menor e mais relevante. O modelo recebe menos contexto disperso e mais evidência concentrada.

3.2 PDFs com tabelas
Divisão em chunks
Separar tabela como unidade própria. Cada chunk deve conter: nome da tabela, cabeçalhos, linhas, notas e vigência. Em tabelas grandes, quebrar por blocos de linhas mantendo cabeçalhos repetidos em cada bloco.

Tamanho recomendado
Entre 250 e 450 tokens por chunk tabular, priorizando legibilidade estrutural em vez de tamanho fixo.

Quando usar overlap
Usar overlap estrutural, não textual: repetir cabeçalhos e notas de rodapé em todos os subchunks. Overlap de conteúdo de linha só quando a linha for quebrada por limite de tamanho.

Aderência às perguntas dos usuários
Excelente para perguntas de consulta direta de valor (SLA por tier, multiplicador regional, faixa de peso, prazo adicional), reduzindo troca de células e erro de interpretação.

Redução de lost in the middle
Ao enviar poucos chunks tabulares com cabeçalho explícito, reduz-se contexto irrelevante e aumenta-se a saliência da célula correta no prompt final.

3.3 Wiki com links internos
Divisão em chunks
Chunking orientado a seção de página, preservando metadados de navegação: página origem, seção, links de entrada e saída. Não quebrar títulos de seção dos respectivos parágrafos de regra.

Tamanho recomendado
Entre 300 e 500 tokens por chunk, com foco em blocos de seção coesos.

Quando usar overlap
Overlap leve de 10% entre seções irmãs quando houver dependência direta. Complementar com expansão por grafo de links no retrieval, em vez de aumentar overlap textual.

Aderência às perguntas dos usuários
Atende bem perguntas de contexto operacional e fluxo (“o que fazer depois”, “qual área aprova”, “qual política complementa esta”), pois o retrieval consegue trazer seção principal e páginas relacionadas.

Redução de lost in the middle
A estratégia desloca esforço para seleção inteligente por grafo e reranking, evitando prompt longo com muitas páginas inteiras.

3.4 Planilhas com fórmulas
Divisão em chunks
Criar dois tipos de chunk:
A. chunk de valor de negócio (tabela de parâmetros, faixas, saídas).
B. chunk de lógica (fórmulas, dependências entre células/abas, condições).
Manter referência cruzada entre A e B pelo mesmo identificador de regra.

Tamanho recomendado
Chunks de 150 a 350 tokens para lógica e 200 a 400 tokens para parâmetros, mantendo cada regra calculável em uma unidade pequena.

Quando usar overlap
Overlap mínimo, apenas quando fórmula depende de múltiplas células contíguas que foram separadas. Priorizar vínculo por metadado de dependência em vez de repetir texto.

Aderência às perguntas dos usuários
Atende perguntas de cálculo e explicação (“como chegou nesse valor?”, “qual desconto aplica?”), permitindo recuperar regra + parâmetro + condição no mesmo fluxo.

Redução de lost in the middle
Chunks curtos e tipados (lógica vs parâmetro) diminuem ruído e tornam o contexto final compacto, com evidências matemáticas mais fáceis de priorizar no topo do prompt.

4. Política de overlap consolidada

Overlap padrão: 10% a 15% para texto corrido com continuidade semântica.
Overlap tabular: repetir cabeçalhos e notas, não duplicar linhas indiscriminadamente.
Overlap em planilhas: usar apenas quando necessário para dependência de fórmula.
Evitar overlap alto global, pois aumenta duplicidade, custo e confusão no reranking.
5. Como a estratégia atende ao retrieval e mitiga lost in the middle

Prioriza chunks semanticamente completos, reduzindo necessidade de top-k alto.
Permite retrieval em dois estágios: busca ampla, depois reranking focado em autoridade e relevância.
Favorece montagem de contexto curto e ordenado por criticidade da evidência.
Diminui documentos longos no prompt final e aumenta densidade informacional útil.
Melhora precisão em perguntas críticas de regra, prazo, SLA e cálculo.
6. Recomendação operacional final

Adotar chunking híbrido por tipo de fonte, não estratégia única para tudo.
Manter metadados ricos: tipo de documento, seção, versão, data, vigência e nível de autoridade.
Usar top-k menor e mais qualificado em produção para reduzir lost in the middle.
Revisar periodicamente tamanhos e overlap com base em métricas de acurácia e groundedness.