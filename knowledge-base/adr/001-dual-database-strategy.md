# ADR-001: Dual Database Strategy (Neo4j + PostgreSQL)

## Status
Accepted

## Context
CrystalClear precisa de modelar dois tipos distintos de dados:
1. Dados operacionais estruturados (utilizadores, declarações, workflows de aprovação)
2. Redes de relações entre entidades com dimensão temporal (o grafo de influência)

Uma base de dados relacional resolve bem o ponto 1 mas é ineficiente para traversals de grafo. Uma base de dados de grafos resolve bem o ponto 2 mas é inadequada para dados transacionais e workflows.

## Decision
Usar PostgreSQL para dados operacionais e Neo4j para o grafo de influência. PostgreSQL é o source of truth; Neo4j é uma projeção otimizada para análise.

## Consequences

### Positivas
- Cada base de dados é usada no contexto para o qual foi desenhada
- Queries de grafo (centralidade, caminhos, clustering) são naturais e eficientes em Neo4j
- Queries transacionais e relatórios são eficientes em PostgreSQL
- O modelo escala independentemente em cada dimensão

### Negativas
- Necessidade de manter sincronização entre as duas bases de dados
- Complexidade operacional acrescida (dois sistemas para gerir)
- Possibilidade de inconsistência temporária entre PostgreSQL e Neo4j

### Mitigação
- A sincronização é unidirecional: PostgreSQL → Neo4j
- Campo `neo4j_synced` em cada item de declaração para rastrear estado de sincronização
- No Sprint 1, a sincronização é síncrona (acontece no momento da validação)
- Em sprints futuros, pode evoluir para event-driven (async)
