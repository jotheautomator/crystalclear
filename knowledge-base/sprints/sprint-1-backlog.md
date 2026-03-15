# Sprint 1 Backlog — CrystalClear

## Visão do Sprint

Construir a fundação da plataforma: autenticação por roles, gestão de entidades de referência, submissão e validação de declarações de interesses, e os primeiros endpoints de análise temporal. No final do Sprint 1, um Political Agent deve conseguir registar-se, submeter uma declaração, e um Journalist deve conseguir consultar a evolução de rendimentos.

## Dependências entre User Stories

```
US01 (register) ─┐
                  ├──► US02 (approve) ──► US06 (submit declaration) ──► US07 (consult)
US04 (institutions)──┘                          │                          │
US05 (functions) ────────────────────────────────┘                          │
                                                                            │
                                         US08 (validate) ◄─────────────────┘
                                              │
                                              ▼
                              ┌────── US09 (integrated situation)
                              ├────── US10 (income evolution)
                              └────── US11 (consult assets)

US03 (list institutions) ── independente (read-only)
US12 (complaint) ── depende apenas de US01/US02
```

## Ordem de execução sugerida

### Fase 1 — Fundação (semanas 1-2)
| Prioridade | US   | Descrição                    | Story Points | Justificação                        |
|------------|------|------------------------------|--------------|-------------------------------------|
| 1          | US01 | Registo de utilizadores      | 5            | Tudo depende de autenticação        |
| 2          | US02 | Aprovação de registos        | 3            | Desbloqueia acesso à plataforma     |
| 3          | US04 | Registar instituições        | 3            | Necessário para declarações         |
| 4          | US05 | Registar funções             | 2            | Necessário para declarações         |

### Fase 2 — Core (semanas 2-3)
| Prioridade | US   | Descrição                    | Story Points | Justificação                        |
|------------|------|------------------------------|--------------|-------------------------------------|
| 5          | US03 | Listar instituições          | 2            | Read-only, simples                  |
| 6          | US06 | Submeter declaração          | 13           | Story mais complexa do sprint       |
| 7          | US07 | Consultar declaração         | 3            | Complemento direto da US06          |

### Fase 3 — Validação e Análise (semanas 3-4)
| Prioridade | US   | Descrição                    | Story Points | Justificação                        |
|------------|------|------------------------------|--------------|-------------------------------------|
| 8          | US08 | Validar declaração           | 5            | Ativa o fluxo completo              |
| 9          | US09 | Situação integrada           | 8            | Primeiro endpoint de análise        |
| 10         | US10 | Evolução de rendimentos      | 8            | Análise temporal                    |
| 11         | US11 | Consultar bens               | 5            | Filtragem por role                  |
| 12         | US12 | Queixa                       | 3            | Independente, pode ser paralela     |

**Total: 60 story points**

## Atribuição de agentes (Matriz de rotação)

| US   | Testes  | Implementação | Review  |
|------|---------|---------------|---------|
| US01 | Atlas   | Bolt          | Cipher  |
| US02 | Bolt    | Cipher        | Atlas   |
| US03 | Cipher  | Atlas         | Bolt    |
| US04 | Atlas   | Cipher        | Bolt    |
| US05 | Bolt    | Atlas         | Cipher  |
| US06 | Cipher  | Bolt          | Atlas   |
| US07 | Atlas   | Bolt          | Cipher  |
| US08 | Bolt    | Cipher        | Atlas   |
| US09 | Cipher  | Atlas         | Bolt    |
| US10 | Atlas   | Cipher        | Bolt    |
| US11 | Bolt    | Atlas         | Cipher  |
| US12 | Cipher  | Bolt          | Atlas   |

---

# User Stories detalhadas

---

## US01 — Registo de utilizadores

**Como** futuro utilizador,
**quero** solicitar registo na plataforma com as permissões adequadas ao meu papel,
**para** poder aceder às funcionalidades correspondentes.

### Prioridade: Must
### Story Points: 5
### UC: Engenharia de Software

### Critérios de aceitação

- [ ] CA1: O utilizador preenche email, password, nome completo e seleciona um role de uma lista predefinida (POLITICAL_AGENT, CITIZEN, JOURNALIST, ETHICS_COMMITTEE).
- [ ] CA2: O role ADMIN não está disponível para auto-registo.
- [ ] CA3: A password é validada: mínimo 8 caracteres, pelo menos uma maiúscula, uma minúscula, um dígito e um caractere especial.
- [ ] CA4: O email é validado quanto ao formato e unicidade.
- [ ] CA5: Após registo, o utilizador fica com status PENDING e não pode fazer login até ser aprovado.
- [ ] CA6: A password é armazenada com hash bcrypt, nunca em texto claro.
- [ ] CA7: O endpoint retorna 201 com os dados do utilizador (sem password) ou 400/409 com erro descritivo.

### Notas técnicas

- Endpoint: `POST /api/v1/auth/register`
- A tabela `users` no PostgreSQL é criada nesta US
- Não criar nó Person no Neo4j nesta fase — apenas quando o admin aprovar (US02)
- Incluir validação Pydantic para o request body

### Dependências: Nenhuma (primeira US)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0101  | Testes        | Atlas  | `tests/unit/test_auth_service.py`, `tests/unit/test_user_schemas.py` |
| T-0102  | Implementação | Bolt   | `app/api/auth.py`, `app/services/auth_service.py`, `app/schemas/user.py`, `app/models/user.py`, `app/repositories/postgres/user_repository.py`, `app/repositories/interfaces/user_repository.py` |
| T-0103  | Review        | Cipher | —                                                                |

---

## US02 — Aprovação de registos

**Como** Administrador,
**quero** aceitar ou rejeitar pedidos de registo,
**para** controlar quem acede à plataforma.

### Prioridade: Must
### Story Points: 3
### UC: Engenharia de Software

### Critérios de aceitação

- [ ] CA1: O admin vê a lista de registos pendentes, paginada.
- [ ] CA2: O admin pode aprovar ou rejeitar cada pedido.
- [ ] CA3: Ao aprovar um POLITICAL_AGENT, é criado um nó Person no Neo4j e o `person_node_id` é gravado na tabela `users`.
- [ ] CA4: Ao rejeitar, o status muda para REJECTED e o utilizador não pode fazer login.
- [ ] CA5: Apenas utilizadores com role ADMIN podem aceder a este endpoint.
- [ ] CA6: O endpoint retorna 200 com o utilizador atualizado ou 403/404 com erro.

### Notas técnicas

- Endpoints: `GET /api/v1/users/registrations`, `PATCH /api/v1/users/registrations/{user_id}`
- Primeira interação com Neo4j — criar nó Person
- Implementar middleware de autorização por role
- Login endpoint (`POST /api/v1/auth/login`) deve ser criado nesta US para o admin poder autenticar-se

### Dependências: US01

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0201  | Testes        | Bolt   | `tests/unit/test_user_service.py`, `tests/unit/test_auth_middleware.py` |
| T-0202  | Implementação | Cipher | `app/api/users.py`, `app/services/user_service.py`, `app/core/security.py`, `app/core/dependencies.py`, `app/repositories/neo4j/person_repository.py`, `app/repositories/interfaces/person_repository.py` |
| T-0203  | Review        | Atlas  | —                                                                |

---

## US03 — Listar instituições

**Como** Agente Político,
**quero** listar as instituições existentes agrupadas por tipo e ordenadas alfabeticamente,
**para** poder referenciá-las ao submeter declarações.

### Prioridade: Should
### Story Points: 2
### UC: POO

### Critérios de aceitação

- [ ] CA1: As instituições são retornadas agrupadas por tipo (COMPANY, POLITICAL_PARTY, FOUNDATION, INSTITUTE, ASSOCIATION).
- [ ] CA2: Dentro de cada grupo, estão ordenadas alfabeticamente por nome.
- [ ] CA3: É possível filtrar por tipo via query parameter.
- [ ] CA4: É possível pesquisar por nome (search parcial, case-insensitive).
- [ ] CA5: A resposta é paginada.
- [ ] CA6: Qualquer utilizador autenticado pode aceder.

### Notas técnicas

- Endpoint: `GET /api/v1/institutions`
- Read-only sobre o Neo4j (nós Institution)
- Pode correr em paralelo com US04

### Dependências: US04 (precisa de instituições registadas para ter dados)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0301  | Testes        | Cipher | `tests/unit/test_institution_service.py`                         |
| T-0302  | Implementação | Atlas  | `app/api/entities.py`, `app/services/institution_service.py`     |
| T-0303  | Review        | Bolt   | —                                                                |

---

## US04 — Registar instituições

**Como** Administrador,
**quero** registar uma instituição de um dado tipo,
**para** que esteja disponível para referência nas declarações.

### Prioridade: Must
### Story Points: 3
### UC: POO

### Critérios de aceitação

- [ ] CA1: O tipo é selecionado de uma lista predefinida (COMPANY, POLITICAL_PARTY, FOUNDATION, INSTITUTE, ASSOCIATION).
- [ ] CA2: O nome é obrigatório e não pode ser duplicado dentro do mesmo tipo.
- [ ] CA3: Tax ID (NIPC) é opcional mas, se fornecido, deve ser único.
- [ ] CA4: A instituição é criada como nó no Neo4j.
- [ ] CA5: Apenas ADMIN pode registar instituições.
- [ ] CA6: O endpoint retorna 201 com a instituição criada ou 400/409 com erro.

### Notas técnicas

- Endpoint: `POST /api/v1/institutions`
- Cria nó Institution no Neo4j
- Definir schema Pydantic para Institution

### Dependências: US02 (necessário admin autenticado)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0401  | Testes        | Atlas  | `tests/unit/test_institution_service.py` (create tests)          |
| T-0402  | Implementação | Cipher | `app/schemas/institution.py`, `app/repositories/neo4j/institution_repository.py`, `app/repositories/interfaces/institution_repository.py` |
| T-0403  | Review        | Bolt   | —                                                                |

---

## US05 — Registar funções

**Como** Administrador,
**quero** registar funções (cargos),
**para** que estejam disponíveis para seleção nas declarações.

### Prioridade: Must
### Story Points: 2
### UC: POO

### Critérios de aceitação

- [ ] CA1: A função tem nome, natureza (PUBLIC, PRIVATE, SOCIAL) e descrição opcional.
- [ ] CA2: O nome é obrigatório e não pode ser duplicado.
- [ ] CA3: A natureza é selecionada de uma lista predefinida.
- [ ] CA4: Apenas ADMIN pode registar funções.
- [ ] CA5: Funções podem ser listadas por qualquer utilizador autenticado.

### Notas técnicas

- Endpoints: `POST /api/v1/functions`, `GET /api/v1/functions`
- Funções são armazenadas no PostgreSQL (tabela `functions`) — são dados de referência, não fazem parte do grafo
- Alternativa: armazenar no Neo4j como nós para permitir queries de grafo que envolvam funções. Decisão: PostgreSQL por simplicidade (são lookup data)

### Dependências: US02 (necessário admin autenticado)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0501  | Testes        | Bolt   | `tests/unit/test_function_service.py`                            |
| T-0502  | Implementação | Atlas  | `app/api/functions.py`, `app/services/function_service.py`, `app/schemas/function.py`, `app/models/function.py`, `app/repositories/postgres/function_repository.py` |
| T-0503  | Review        | Cipher | —                                                                |

---

## US06 — Submeter declaração de interesses

**Como** Agente Político,
**quero** submeter uma declaração de interesses incluindo rendimentos, cargos, bens e participações,
**para** cumprir as minhas obrigações de transparência.

### Prioridade: Must
### Story Points: 13
### UC: Engenharia de Software + POO

### Critérios de aceitação

- [ ] CA1: A declaração inclui tipo (INITIAL, REGULAR, EXCEPTIONAL) e data de referência.
- [ ] CA2: A declaração contém secções: posições/cargos, bens patrimoniais, participações empresariais, apoios/subsídios.
- [ ] CA3: Cada posição referencia uma instituição existente e uma função existente.
- [ ] CA4: Cada participação referencia uma instituição existente do tipo COMPANY.
- [ ] CA5: Cada apoio referencia uma instituição existente.
- [ ] CA6: Valores monetários são validados (não negativos).
- [ ] CA7: Datas são validadas (start_date < end_date quando ambas existem).
- [ ] CA8: A declaração é criada no PostgreSQL com status SUBMITTED.
- [ ] CA9: As relações correspondentes são criadas no Neo4j com as datas temporais (valid_from, valid_to) derivadas dos dados da declaração.
- [ ] CA10: Apenas POLITICAL_AGENT pode submeter declarações.
- [ ] CA11: O political agent só pode submeter declarações em seu próprio nome.

### Notas técnicas

- Endpoint: `POST /api/v1/declarations`
- Esta é a US mais complexa: envolve PostgreSQL (metadados da declaração) e Neo4j (relações do grafo)
- Transação cross-database: se a escrita no Neo4j falhar, a declaração no PostgreSQL deve ficar marcada como falhada ou ser revertida
- As relações criadas no Neo4j devem incluir referência ao ID da declaração para rastreabilidade

### Dependências: US01, US02, US04, US05

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0601  | Testes        | Cipher | `tests/unit/test_declaration_service.py`, `tests/unit/test_declaration_schemas.py` |
| T-0602  | Implementação | Bolt   | `app/api/declarations.py`, `app/services/declaration_service.py`, `app/schemas/declaration.py`, `app/models/declaration.py`, `app/repositories/postgres/declaration_repository.py`, `app/repositories/interfaces/declaration_repository.py`, `app/repositories/neo4j/graph_writer.py` |
| T-0603  | Review        | Atlas  | —                                                                |

---

## US07 — Consultar declaração submetida

**Como** Agente Político,
**quero** consultar uma declaração de interesses previamente submetida,
**para** verificar os dados que declarei.

### Prioridade: Must
### Story Points: 3
### UC: POO

### Critérios de aceitação

- [ ] CA1: O agente político vê a lista das suas declarações, paginada e ordenada por data.
- [ ] CA2: Pode consultar o detalhe de cada declaração com todas as secções (posições, bens, participações, apoios).
- [ ] CA3: Vê o status atual da declaração (SUBMITTED, UNDER_REVIEW, VALIDATED, REJECTED).
- [ ] CA4: Se rejeitada, vê os comentários do Ethics Committee.
- [ ] CA5: Um agente político só pode consultar as suas próprias declarações.
- [ ] CA6: Ethics Committee e Admin podem consultar declarações de qualquer agente.

### Notas técnicas

- Endpoints: `GET /api/v1/declarations`, `GET /api/v1/declarations/{id}`
- Os dados vêm do PostgreSQL (metadados + status) e do Neo4j (conteúdo das relações)
- Considerar cache para declarações validadas (dados imutáveis)

### Dependências: US06

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0701  | Testes        | Atlas  | `tests/unit/test_declaration_service.py` (read tests)            |
| T-0702  | Implementação | Bolt   | Extensão dos ficheiros da US06 + `app/repositories/neo4j/graph_reader.py` |
| T-0703  | Review        | Cipher | —                                                                |

---

## US08 — Validar declaração de interesses

**Como** membro da Comissão de Ética,
**quero** validar ou rejeitar uma declaração de interesses submetida,
**para** garantir a correção e completude dos dados declarados.

### Prioridade: Must
### Story Points: 5
### UC: Engenharia de Software

### Critérios de aceitação

- [ ] CA1: A comissão de ética vê a lista de declarações com status SUBMITTED, paginada.
- [ ] CA2: Ao validar, o status muda para VALIDATED e a data de validação é registada.
- [ ] CA3: Ao rejeitar, o status muda para REJECTED e comentários são obrigatórios.
- [ ] CA4: Os comentários de rejeição indicam a secção específica (positions, assets, participations, supports) e o problema.
- [ ] CA5: Após validação, as relações no Neo4j ficam marcadas como confirmadas.
- [ ] CA6: Apenas ETHICS_COMMITTEE pode validar/rejeitar declarações.

### Notas técnicas

- Endpoint: `POST /api/v1/declarations/{id}/validation`
- Actualiza PostgreSQL (status, comments) e Neo4j (flag de confirmação nas relações)
- Criar tabela `declaration_comments` no PostgreSQL
- Registar ação no audit_log

### Dependências: US06, US07

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0801  | Testes        | Bolt   | `tests/unit/test_validation_service.py`                          |
| T-0802  | Implementação | Cipher | `app/api/validation.py`, `app/services/validation_service.py`, `app/schemas/validation.py`, `app/models/declaration_comment.py` |
| T-0803  | Review        | Atlas  | —                                                                |

---

## US09 — Situação integrada de um agente político

**Como** membro da Comissão de Ética,
**quero** consultar a situação integrada de um agente político numa data específica,
**para** ter uma visão completa das suas posições, bens e participações nesse momento.

### Prioridade: Must
### Story Points: 8
### UC: Matemática Discreta + Estatística

### Critérios de aceitação

- [ ] CA1: Dado um agente político e uma data, o sistema retorna todas as posições ativas nessa data.
- [ ] CA2: Retorna todos os bens detidos nessa data com valores estimados.
- [ ] CA3: Retorna todas as participações empresariais ativas nessa data.
- [ ] CA4: Retorna todos os apoios/subsídios ativos nessa data.
- [ ] CA5: Calcula totais: rendimento total, valor total de bens, valor total de participações.
- [ ] CA6: Apenas dados de declarações VALIDATED são considerados.
- [ ] CA7: Apenas ETHICS_COMMITTEE pode aceder a este endpoint.

### Notas técnicas

- Endpoint: `GET /api/v1/analysis/integrated-situation/{person_id}?date=YYYY-MM-DD`
- Primeiro endpoint que usa o temporal snapshot do Neo4j
- Usa o filtro: `WHERE r.valid_from <= date AND (r.valid_to IS NULL OR r.valid_to >= date)`
- Início do Graph Engine — criar módulo `app/graph/`

### Dependências: US06, US08

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-0901  | Testes        | Cipher | `tests/unit/test_analysis_service.py`, `tests/unit/test_graph_engine.py` |
| T-0902  | Implementação | Atlas  | `app/api/analysis.py`, `app/services/analysis_service.py`, `app/graph/temporal.py`, `app/graph/snapshot.py` |
| T-0903  | Review        | Bolt   | —                                                                |

---

## US10 — Evolução de rendimentos

**Como** jornalista,
**quero** analisar a evolução dos rendimentos de um agente político entre duas datas,
**para** investigar alterações significativas de rendimento.

### Prioridade: Must
### Story Points: 8
### UC: Estatística + Matemática Discreta

### Critérios de aceitação

- [ ] CA1: Dado um agente político e um intervalo de datas, o sistema retorna uma timeline de rendimentos.
- [ ] CA2: Cada ponto na timeline inclui as posições ativas e o rendimento total nesse momento.
- [ ] CA3: Os pontos da timeline correspondem a datas em que houve mudanças (início/fim de posição).
- [ ] CA4: O summary inclui: rendimento no início do período, rendimento no fim, variação absoluta e percentual.
- [ ] CA5: Apenas dados de declarações VALIDATED são considerados.
- [ ] CA6: Apenas JOURNALIST pode aceder a este endpoint.

### Notas técnicas

- Endpoint: `GET /api/v1/analysis/income-evolution/{person_id}?from=YYYY-MM-DD&to=YYYY-MM-DD`
- Requer identificar todos os "eventos" (inícios e fins de posições) dentro do intervalo
- Reutiliza lógica do Graph Engine criado na US09
- Considerar edge case: período sem qualquer posição

### Dependências: US09 (reutiliza Graph Engine)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-1001  | Testes        | Atlas  | `tests/unit/test_income_analysis.py`                             |
| T-1002  | Implementação | Cipher | Extensão de `app/services/analysis_service.py`, `app/graph/evolution.py` |
| T-1003  | Review        | Bolt   | —                                                                |

---

## US11 — Consultar bens de um agente político

**Como** cidadão ou jornalista,
**quero** consultar os bens patrimoniais de um agente político numa data específica,
**para** exercer escrutínio público.

### Prioridade: Must
### Story Points: 5
### UC: Engenharia de Software

### Critérios de aceitação

- [ ] CA1: Dado um agente político e uma data, retorna os bens detidos nessa data.
- [ ] CA2: Para JOURNALIST: todos os campos são visíveis, incluindo estimated_value.
- [ ] CA3: Para CITIZEN: estimated_value é parcialmente omitido (ex: mostrar apenas a faixa de valor, não o valor exato).
- [ ] CA4: Cada bem inclui tipo, descrição e localização.
- [ ] CA5: Apenas dados de declarações VALIDATED são considerados.
- [ ] CA6: Apenas CITIZEN e JOURNALIST podem aceder.

### Notas técnicas

- Endpoint: `GET /api/v1/analysis/assets/{person_id}?date=YYYY-MM-DD`
- Implementar filtragem de dados sensíveis na Service Layer baseada no role do utilizador
- Definir faixas de valor para cidadãos (ex: < 100k, 100k-500k, 500k-1M, > 1M)
- Reutiliza snapshot temporal do Graph Engine

### Dependências: US09 (reutiliza Graph Engine)

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-1101  | Testes        | Bolt   | `tests/unit/test_asset_analysis.py`                              |
| T-1102  | Implementação | Atlas  | Extensão de `app/services/analysis_service.py`, `app/schemas/analysis.py` |
| T-1103  | Review        | Cipher | —                                                                |

---

## US12 — Queixa sobre agente político

**Como** cidadão,
**quero** apresentar uma queixa sobre um agente político relativamente a um cargo específico e data,
**para** reportar situações de falta de transparência.

### Prioridade: Should
### Story Points: 3
### UC: Engenharia de Software

### Critérios de aceitação

- [ ] CA1: O cidadão seleciona o agente político alvo da queixa.
- [ ] CA2: Indica o cargo/função e a data a que se refere.
- [ ] CA3: Escreve uma descrição da queixa (campo livre, obrigatório, mínimo 50 caracteres).
- [ ] CA4: A queixa é criada com status OPEN.
- [ ] CA5: Apenas CITIZEN pode submeter queixas.
- [ ] CA6: O endpoint retorna 201 com a queixa criada.

### Notas técnicas

- Endpoint: `POST /api/v1/complaints`
- Armazenada no PostgreSQL (tabela `complaints`)
- Referência ao Person node no Neo4j via `target_person` UUID
- Registar no audit_log

### Dependências: US01, US02

### Tarefas

| Task ID | Fase          | Agente | Ficheiros                                                        |
|---------|---------------|--------|------------------------------------------------------------------|
| T-1201  | Testes        | Cipher | `tests/unit/test_complaint_service.py`                           |
| T-1202  | Implementação | Bolt   | `app/api/complaints.py`, `app/services/complaint_service.py`, `app/schemas/complaint.py`, `app/models/complaint.py`, `app/repositories/postgres/complaint_repository.py` |
| T-1203  | Review        | Atlas  | —                                                                |
