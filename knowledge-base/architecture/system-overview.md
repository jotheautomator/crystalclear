# System Overview — CrystalClear

## Visão Geral

CrystalClear é uma plataforma de análise e visualização de redes de influência política com dimensão temporal. O sistema mapeia relações entre agentes políticos, instituições, património e funções, permitindo observar a evolução destas redes ao longo do tempo.

## Arquitectura de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
│                    React + TypeScript                           │
│                                                                 │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌────────────┐   │
│  │   Auth   │  │ Declarations │  │ Analysis │  │   Graph    │   │
│  │  Module  │  │    Module    │  │  Module  │  │ Visualizer │   │ 
│  └──────────┘  └──────────────┘  └──────────┘  └────────────┘   │
│                                                  Cytoscape.js   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API (JSON)
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│                        BACKEND                                  │
│                    Python + FastAPI                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Layer (Routers)                   │   │
│  │  /auth  /users  /institutions  /declarations  /analysis  │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐   │
│  │                  Application Layer (Services)            │   │
│  │  AuthService  DeclarationService  AnalysisService        │   │
│  │  UserService  InstitutionService  GraphService           │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐   │
│  │                    Domain Layer (Models)                 │   │
│  │  PoliticalAgent  Institution  Declaration  Asset         │   │
│  │  Position  BusinessParticipation  Complaint  Function    │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐   │
│  │               Infrastructure Layer (Repositories)        │   │
│  │  Neo4jRepository  PostgresRepository                     │   │
│  │  (grafos/relações)  (dados estruturados)                 │   │
│  └─────────┬────────────────────────────────┬───────────────┘   │
└────────────┼────────────────────────────────┼───────────────────┘
             │                                │
     ┌───────┴───────┐              ┌─────────┴────────┐
     │    Neo4j      │              │   PostgreSQL     │
     │  (Relações,   │              │  (Users, Auth,   │
     │   Redes,      │              │   Declarations,  │
     │   Temporal)   │              │   Complaints)    │
     └───────────────┘              └──────────────────┘
```

## Camadas

### API Layer
Responsável por receber requests HTTP, validar input (via Pydantic), delegar ao service correto, e devolver responses formatadas. Não contém lógica de negócio.

### Application Layer (Services)
Contém a lógica de negócio e orquestra operações entre repositórios. Um service pode usar múltiplos repositories. É aqui que vivem as regras de validação de declarações, cálculo de métricas, e lógica de análise temporal.

### Domain Layer (Models)
Modelos puros do domínio. Não dependem de nenhuma framework ou base de dados. Representam as entidades do problema: agentes políticos, instituições, declarações, ativos, etc.

### Infrastructure Layer (Repositories)
Implementações concretas de persistência. Abstrai o acesso às bases de dados atrás de interfaces (protocols em Python). Permite que os services não saibam se estão a falar com Neo4j, PostgreSQL, ou um mock.

## Separação de Responsabilidades entre Bases de Dados

### Neo4j — O Grafo de Influência

Neo4j é responsável por modelar e persistir o grafo de relações entre entidades. Tudo o que é "quem se relaciona com quem, como, e quando" vive aqui.

Nós (Nodes):
- PoliticalAgent
- Institution (com label adicional: Company, Party, Foundation, Association, Institute)
- Asset (com label: RealEstate, Shares, Quotas)
- Function/Position

Relações (Edges) — todas com propriedades temporais (start_date, end_date):
- HOLDS_POSITION (PoliticalAgent → Institution)
- OWNS (PoliticalAgent → Asset)
- HAS_PARTICIPATION (PoliticalAgent → Institution)
- RECEIVES_SUPPORT (PoliticalAgent → Institution)
- MEMBER_OF (PoliticalAgent → Institution)

A dimensão temporal é implementada como propriedades nas relações, permitindo queries como "que posições tinha o agente X na data Y" ou "como evoluiu a rede de influência entre 2020 e 2024".

### PostgreSQL — Dados Operacionais

PostgreSQL é responsável por dados estruturados que não são naturalmente modeláveis como grafo:

- Users (autenticação, roles, credenciais)
- Registration requests (workflow de aprovação)
- Declarations (metadados, status, workflow de validação)
- Declaration items (linhas de rendimento, posições, ativos — referenciados depois no grafo)
- Complaints (denúncias de cidadãos)
- Audit log (quem fez o quê e quando)

### Sincronização

Quando uma declaração é submetida e validada, os dados relevantes são projetados para o Neo4j como nós e relações. O PostgreSQL é o source of truth para dados operacionais; o Neo4j é a projeção otimizada para análise de grafos.

## Autenticação e Autorização

- JWT com access token (curta duração) e refresh token
- Roles: ADMIN, POLITICAL_AGENT, CITIZEN, JOURNALIST, ETHICS_COMMITTEE
- Permissions mapeadas por role
- Dados sensíveis filtrados na API Layer consoante o role do user autenticado

## Padrões Arquitecturais

- **Repository Pattern**: abstrai persistência, facilita testing com mocks
- **Service Layer**: isola lógica de negócio da framework web
- **Dependency Injection**: FastAPI's Depends() para injetar services e repositories
- **DTO/Schema separation**: Pydantic schemas para API, modelos de domínio internos separados
- **Event-driven sync**: declaração validada → evento → projeção para Neo4j (pode ser síncrono no Sprint 1, assíncrono depois)
