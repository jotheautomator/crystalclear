# Relationships — CrystalClear

## Grafo de Relações (Neo4j)

Todas as relações do grafo de influência são temporais — possuem `start_date` e `end_date` (nullable, significando "ainda ativo").

```
PoliticalAgent ──HOLDS_POSITION──▶ Institution
    │                                    ▲
    ├──OWNS──▶ Asset                     │
    │                                    │
    ├──HAS_PARTICIPATION─────────────────┘
    │
    └──RECEIVES_SUPPORT──▶ Institution
```

### HOLDS_POSITION
- Origem: PoliticalAgent
- Destino: Institution
- Semântica: "O agente exerce/exerceu uma função nesta instituição"
- Propriedades: function, nature, payment, start_date, end_date, declaration_id
- Multiplicidade: Um agente pode ter múltiplas posições em múltiplas instituições (e ao longo do tempo)

### OWNS
- Origem: PoliticalAgent
- Destino: Asset
- Semântica: "O agente possui/possuiu este ativo"
- Propriedades: estimated_value, acquisition_date, declaration_date, declaration_id
- Nota: O valor pode mudar entre declarações — cada declaração cria um snapshot

### HAS_PARTICIPATION
- Origem: PoliticalAgent
- Destino: Institution
- Semântica: "O agente detém/deteve participação nesta empresa"
- Propriedades: type, market_value, percentage, declaration_date, declaration_id

### RECEIVES_SUPPORT
- Origem: PoliticalAgent
- Destino: Institution
- Semântica: "O agente recebeu apoio/subsídio desta instituição"
- Propriedades: amount, description, declaration_date, declaration_id

## Relações Operacionais (PostgreSQL)

Estas relações são implementadas via foreign keys no PostgreSQL.

```
User ──submits──▶ Declaration ──contains──▶ Position
  │                   │                     Asset
  │                   │                     Participation
  │                   │                     Support
  │                   │
  │                   ├──reviewed_by──▶ User (Ethics Committee)
  │                   └──has──▶ DeclarationReview
  │
  ├──submits──▶ Complaint ──targets──▶ User (Political Agent)
  │
  └──reviews──▶ RegistrationRequest
```

### User → Declaration (1:N)
Um agente político pode ter múltiplas declarações ao longo do tempo.

### Declaration → Items (1:N)
Uma declaração contém múltiplos itens de cada tipo (positions, assets, participations, supports).

### User → Complaint (N:1 em ambos os lados)
Um cidadão pode submeter múltiplas queixas. Um agente político pode ser alvo de múltiplas queixas.

### User → RegistrationRequest (1:1)
Cada pedido de registo resulta (se aprovado) na criação de um User.

## Dimensão Temporal

A dimensão temporal opera em dois níveis:

### Nível 1 — Relações com duração
Posições (HOLDS_POSITION) têm start_date e end_date, representando o período em que o agente exerceu essa função. Isto permite queries como "quem era ministro em Março de 2022?"

### Nível 2 — Snapshots por declaração
Ativos, participações e apoios são registados por declaração. Cada declaração é um snapshot da situação do agente na data de referência. Comparando declarações ao longo do tempo, é possível detetar evolução patrimonial.

### Implicações para queries
- **Situação numa data (US09):** Filtrar relações onde `start_date ≤ data AND (end_date IS NULL OR end_date ≥ data)`
- **Evolução entre datas (US10):** Filtrar relações cujo período intersecta o intervalo [data_inicio, data_fim]
- **Património numa data (US11):** Encontrar a declaração mais recente anterior à data e retornar os seus ativos
