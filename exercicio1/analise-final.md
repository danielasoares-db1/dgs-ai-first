Revisão Crítica da Análise RAG - Cenário NovaTech

Objetivo
Esta revisão consolida riscos arquiteturais e operacionais não totalmente endereçados na análise anterior, com foco em robustez de produção para um sistema RAG em domínio normativo. Para cada ponto, são apresentados: risco, impacto e melhoria recomendada.

1) Governança de versões e vigência insuficiente
Risco
A análise reconhece conflito documental (ex.: versões de procedimento), mas não define um mecanismo determinístico para decidir qual regra é aplicável por data, escopo e exceção.

Impacto
Respostas inconsistentes entre atendimentos, aplicação de regra revogada e aumento de risco de não conformidade.

Melhoria
Implementar uma camada de policy engine com precedência explícita por autoridade da fonte, vigência, escopo e exceções. Toda resposta deve retornar regra aplicada, versão e justificativa da seleção.

2) Estimativa de tokens otimista e pouco robusta
Risco
A estimativa usa média fixa de conversão palavra/token e não captura variabilidade real de OCR, tabelas, anexos e metadados.

Impacto
Subdimensionamento de custo, latência, armazenamento e capacidade de indexação.

Melhoria
Executar amostragem estratificada por tipo documental com tokenização real do modelo-alvo e reportar faixas P50/P90/P95, não apenas valor médio.

3) Suposição de chunk médio estável
Risco
Assumir chunk médio único (ex.: 500 tokens) em base heterogênea ignora comportamento distinto entre regras, tabelas e wiki interligada.

Impacto
Perda de recall em consultas complexas e aumento de ruído em consultas simples.

Melhoria
Adotar chunking adaptativo por tipo de documento e por intenção da pergunta, validado por benchmark offline com perguntas reais.

4) OCR sem critérios operacionais de bloqueio
Risco
Há recomendação de OCR com confiança por bloco, mas sem thresholds de aceite, quarentena e criticidade por campo.

Impacto
Datas, percentuais e prazos podem ser indexados incorretamente com aparência de confiabilidade.

Melhoria
Definir gates de ingestão (confiança mínima por bloco/campo crítico), quarentena automática de páginas abaixo do limiar e revisão humana mandatória para documentos normativos críticos.

5) Tabelas complexas multi-página e notas legais subtratadas
Risco
A estratégia tabular proposta não detalha reconstrução robusta para tabelas quebradas, células mescladas complexas e notas de rodapé normativas.

Impacto
Troca de células, interpretação incorreta de faixas e aplicação errada de SLA/multiplicadores.

Melhoria
Usar parser com reconstrução de grade lógica, normalização de cabeçalhos hierárquicos e validações por constraints de negócio (faixas, unicidade, consistência).

6) Limitações de chunking para regras compostas
Risco
Chunking por seção pode separar condição, exceção e vigência, que deveriam ser lidas como uma única unidade decisória.

Impacto
Respostas parcialmente corretas, porém erradas em casos de borda.

Melhoria
Criar atomic policy chunks contendo regra + condição + exceção + vigência + fonte, com links explícitos para trechos correlatos.

7) Retrieval sem metas quantitativas de qualidade
Risco
A recomendação de busca híbrida e reranking não traz metas nem critérios de aceite objetivos.

Impacto
Evolução por percepção subjetiva e dificuldade de comprovar ganho real de qualidade.

Melhoria
Estabelecer avaliação contínua com Recall@k, nDCG, groundedness e faithfulness, com gates para promoção entre ambientes.

8) Hierarquia de autoridade pouco operacionalizada no retrieval
Risco
Sem penalização forte por tipo de fonte, trechos de FAQ podem superar documentos normativos por similaridade semântica.

Impacto
Respostas plausíveis porém não conformes com política/contrato.

Melhoria
Incluir score de autoridade documental no reranking e filtro por tipo de fonte conforme intenção da pergunta (normativo > contratual > procedimento > FAQ).

9) Mitigação de lost in the middle incompleta
Risco
A análise reconhece o fenômeno, mas não especifica montagem final de contexto para evidências conflitantes.

Impacto
Trechos críticos posicionados no meio do prompt podem ser subutilizados.

Melhoria
Aplicar prompt assembly por blocos priorizados: evidência normativa principal, contraste de conflito, evidência complementar, e FAQ por último; manter contexto final compacto.

10) Falta de fallback seguro para baixa evidência
Risco
Não há regra explícita para recusar resposta, pedir clarificação ou escalar humano quando evidência for insuficiente/conflitante.

Impacto
Maior probabilidade de alucinação operacional em casos ambíguos.

Melhoria
Definir política de resposta segura baseada em score de evidência e conflito, com quatro estados: responder, responder com ressalva, pedir contexto adicional, escalar.

11) Desafios de produção subestimados
Risco
A análise não aprofunda operação contínua: reindex incremental seguro, rollback de índice, capacidade, custo de embeddings e resposta a incidentes.

Impacto
Degradação de qualidade ao longo do tempo, indisponibilidade e custos acima do previsto.

Melhoria
Implementar runbook de produção com SLOs de latência/qualidade, alertas, canário de índice, versionamento e rollback de ingestão/retrieval.

12) Segurança, privacidade e controle de acesso ausentes
Risco
Não há tratamento explícito de PII, segregação por perfil e trilha de auditoria de consultas/respostas.

Impacto
Risco de vazamento de dados e não conformidade regulatória/contratual.

Melhoria
Aplicar classificação e mascaramento de dados sensíveis na ingestão, ACL por documento/campo no retrieval e logging auditável ponta a ponta.

13) Perguntas multi-hop não contempladas operacionalmente
Risco
Consultas que exigem combinação de múltiplas fontes (política + tabela + exceção) podem falhar com retrieval de um único estágio.

Impacto
Resposta correta em partes, mas incorreta na decisão final.

Melhoria
Adotar recuperação multi-estágio com planejamento de evidências, iteração de busca e verificação cruzada antes da resposta.

14) Ausência de avaliação por criticidade de negócio
Risco
Todos os casos tendem a ser avaliados com o mesmo peso, inclusive cenários de alto impacto contratual/regulatório.

Impacto
Boa média global, mas falhas justamente onde o erro custa mais.

Melhoria
Criar taxonomia de criticidade e thresholds diferenciados por classe de risco, exigindo maior evidência para decisões críticas.

Priorização Recomendada (30/60/90 dias)

0-30 dias (controle de risco imediato)
- Definir hierarquia de fontes e regra de precedência por vigência.
- Implantar fallback seguro (responder com ressalva, pedir contexto, escalar).
- Criar avaliação mínima com conjunto de perguntas críticas e métricas base.

31-60 dias (robustez de ingestão e retrieval)
- Implementar gates de OCR e fluxo de quarentena/revisão humana.
- Evoluir parser tabular com validações de consistência.
- Ativar reranking com autoridade documental e reordenação para mitigar lost in the middle.

61-90 dias (maturidade operacional)
- Estabelecer runbook/SLOs e observabilidade ponta a ponta.
- Implementar versionamento, canário e rollback de índice.
- Introduzir pipeline multi-hop para consultas compostas e testes de regressão contínuos.

Conclusão Executiva
A análise original está tecnicamente correta em fundamentos, mas otimista para operação real em domínio sensível. O principal ganho agora não vem de aumentar contexto, e sim de reforçar governança de evidência, qualidade de extração, política de decisão e disciplina operacional de produção.
