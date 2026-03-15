# Data Model — CrystalClear

## 1. PostgreSQL Schema

### 1.1 Users & Auth

```sql
users
├── id              UUID PRIMARY KEY
├── email           VARCHAR UNIQUE NOT NULL
├── password_hash   VARCHAR NOT NULL
├── full_name       VARCHAR NOT NULL
├── role            ENUM('admin', 'political_agent', 'citizen', 'journalist', 'ethics_committee')
├── is_active       BOOLEAN DEFAULT true
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP

registration_requests
├── id              UUID PRIMARY KEY
├── email           VARCHAR NOT NULL
├── full_name       VARCHAR NOT NULL
├── requested_role  ENUM(...)
├── status          ENUM('pending', 'approved', 'rejected')
├── reviewed_by     UUID FK → users.id (nullable)
├── reviewed_at     TIMESTAMP (nullable)
├── rejection_reason TEXT (nullable)
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP
```

### 1.2 Declarations

```sql
declarations
├── id              UUID PRIMARY KEY
├── political_agent_id  UUID FK → users.id
├── type            ENUM('initial', 'regular', 'exceptional')
├── reference_date  DATE
├── status          ENUM('draft', 'submitted', 'validated', 'rejected')
├── submitted_at    TIMESTAMP (nullable)
├── validated_by    UUID FK → users.id (nullable)
├── validated_at    TIMESTAMP (nullable)
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP

declaration_positions
├── id              UUID PRIMARY KEY
├── declaration_id  UUID FK → declarations.id
├── institution_name VARCHAR NOT NULL
├── institution_type ENUM('company', 'party', 'foundation', 'institute', 'association', 'public_body')
├── function_title  VARCHAR NOT NULL
├── nature          ENUM('public', 'private', 'social')
├── payment         DECIMAL (nullable)
├── start_date      DATE
├── end_date        DATE (nullable)
└── neo4j_synced    BOOLEAN DEFAULT false

declaration_assets
├── id              UUID PRIMARY KEY
├── declaration_id  UUID FK → declarations.id
├── asset_type      ENUM('urban_real_estate', 'rural_real_estate')
├── description     TEXT
├── estimated_value DECIMAL
├── acquisition_date DATE (nullable)
└── neo4j_synced    BOOLEAN DEFAULT false

declaration_participations
├── id              UUID PRIMARY KEY
├── declaration_id  UUID FK → declarations.id
├── institution_name VARCHAR NOT NULL
├── participation_type ENUM('quotas', 'shares', 'holdings')
├── market_value    DECIMAL
├── percentage      DECIMAL (nullable)
└── neo4j_synced    BOOLEAN DEFAULT false

declaration_supports
├── id              UUID PRIMARY KEY
├── declaration_id  UUID FK → declarations.id
├── institution_name VARCHAR NOT NULL
├── institution_type ENUM(...)
├── amount          DECIMAL
├── description     TEXT (nullable)
└── neo4j_synced    BOOLEAN DEFAULT false

declaration_reviews
├── id              UUID PRIMARY KEY
├── declaration_id  UUID FK → declarations.id
├── reviewer_id     UUID FK → users.id
├── section         VARCHAR NOT NULL
├── item_id         UUID (nullable — referência ao item específico)
├── comment         TEXT NOT NULL
├── status          ENUM('flagged', 'resolved')
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP
```

### 1.3 Complaints

```sql
complaints
├── id              UUID PRIMARY KEY
├── complainant_id  UUID FK → users.id
├── political_agent_id UUID FK → users.id
├── agent_role      VARCHAR NOT NULL
├── reference_date  DATE NOT NULL
├── description     TEXT NOT NULL
├── status          ENUM('submitted', 'under_review', 'resolved', 'dismissed')
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP
```

### 1.4 Institutions & Functions (Reference Data)

```sql
institutions
├── id              UUID PRIMARY KEY
├── name            VARCHAR UNIQUE NOT NULL
├── type            ENUM('company', 'party', 'foundation', 'institute', 'association', 'public_body')
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP

functions
├── id              UUID PRIMARY KEY
├── title           VARCHAR UNIQUE NOT NULL
├── description     TEXT (nullable)
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP
```

### 1.5 Audit

```sql
audit_log
├── id              UUID PRIMARY KEY
├── user_id         UUID FK → users.id
├── action          VARCHAR NOT NULL
├── entity_type     VARCHAR NOT NULL
├── entity_id       UUID NOT NULL
├── details         JSONB (nullable)
├── created_at      TIMESTAMP
```

## 2. Neo4j Schema (Grafo de Influência)

### 2.1 Nós (Nodes)

```cypher
(:PoliticalAgent {
    pg_user_id: UUID,       // referência ao PostgreSQL
    name: String,
    current_role: String
})

(:Institution {
    pg_institution_id: UUID,
    name: String,
    type: String            // 'company', 'party', 'foundation', etc.
})
// Labels adicionais: :Company, :Party, :Foundation, :Association, :Institute, :PublicBody

(:Asset {
    pg_asset_id: UUID,
    type: String,           // 'urban_real_estate', 'rural_real_estate'
    description: String,
    estimated_value: Float
})

(:Function {
    pg_function_id: UUID,
    title: String
})
```

### 2.2 Relações (Edges) — Todas Temporais

```cypher
(:PoliticalAgent)-[:HOLDS_POSITION {
    function: String,
    nature: String,         // 'public', 'private', 'social'
    payment: Float,
    start_date: Date,
    end_date: Date,         // null = ainda ativo
    declaration_id: UUID    // rastreabilidade ao PostgreSQL
}]->(:Institution)

(:PoliticalAgent)-[:OWNS {
    estimated_value: Float,
    acquisition_date: Date,
    declaration_date: Date,
    declaration_id: UUID
}]->(:Asset)

(:PoliticalAgent)-[:HAS_PARTICIPATION {
    type: String,           // 'quotas', 'shares', 'holdings'
    market_value: Float,
    percentage: Float,
    declaration_date: Date,
    declaration_id: UUID
}]->(:Institution)

(:PoliticalAgent)-[:RECEIVES_SUPPORT {
    amount: Float,
    description: String,
    declaration_date: Date,
    declaration_id: UUID
}]->(:Institution)
```

### 2.3 Índices Recomendados

```cypher
CREATE INDEX FOR (p:PoliticalAgent) ON (p.pg_user_id);
CREATE INDEX FOR (i:Institution) ON (i.pg_institution_id);
CREATE INDEX FOR (i:Institution) ON (i.name);
CREATE INDEX FOR (a:Asset) ON (a.pg_asset_id);
```

## 3. Fluxo de Sincronização PostgreSQL → Neo4j

```
Declaração submetida (PostgreSQL)
        │
        ▼
Declaração validada pela Ethics Committee
        │
        ▼
Serviço de sincronização:
  1. Cria/atualiza nó PoliticalAgent
  2. Para cada position → cria/atualiza nó Institution + relação HOLDS_POSITION
  3. Para cada asset → cria nó Asset + relação OWNS
  4. Para cada participation → cria/atualiza nó Institution + relação HAS_PARTICIPATION
  5. Para cada support → cria/atualiza nó Institution + relação RECEIVES_SUPPORT
  6. Marca items como neo4j_synced = true
```

## 4. Queries Temporais (Exemplos)

```cypher
// Situação integrada de um agente numa data específica (US09)
MATCH (p:PoliticalAgent {pg_user_id: $agent_id})-[r]->(target)
WHERE r.start_date <= $date AND (r.end_date IS NULL OR r.end_date >= $date)
RETURN p, r, target

// Evolução de rendimento entre duas datas (US10)
MATCH (p:PoliticalAgent {pg_user_id: $agent_id})-[r:HOLDS_POSITION]->(i:Institution)
WHERE r.start_date <= $end_date AND (r.end_date IS NULL OR r.end_date >= $start_date)
RETURN i.name, r.function, r.payment, r.start_date, r.end_date
ORDER BY r.start_date

// Património numa data específica (US11)
MATCH (p:PoliticalAgent {pg_user_id: $agent_id})-[r:OWNS]->(a:Asset)
WHERE r.declaration_date <= $date
RETURN a.type, a.description, a.estimated_value, r.declaration_date
ORDER BY r.declaration_date DESC
```
