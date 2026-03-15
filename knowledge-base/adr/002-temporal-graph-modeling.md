# ADR-002: Temporal Graph Modeling via Edge Properties

## Status
Accepted

## Context
O CrystalClear precisa de representar a evolução de relações ao longo do tempo. Existem várias abordagens para grafos temporais:
1. **Snapshots**: criar cópias completas do grafo para cada momento
2. **Event-based**: registar cada evento de criação/remoção de arestas
3. **Edge properties**: adicionar valid_from/valid_to a cada aresta

## Decision
Usar propriedades temporais (valid_from, valid_to) em todas as relações do Neo4j.

## Rationale
- Snapshots: simples de consultar mas muito ineficiente em espaço (duplicação massiva)
- Event-based: eficiente mas complexo de reconstruir o estado num momento
- Edge properties: bom equilíbrio — consultas temporais via filtro WHERE, sem duplicação, permite tanto snapshots como diffs

Uma relação com `valid_to = null` está ativa. Para reconstruir o grafo na data D, basta filtrar: `WHERE valid_from <= D AND (valid_to IS NULL OR valid_to >= D)`.

## Consequences
- Todas as queries sobre o grafo devem incluir o filtro temporal — risco de esquecimento
- Criar helper functions/queries parametrizadas para encapsular o filtro
- Não permite múltiplas versões da mesma relação no mesmo período (sem overlap)
- Necessário validar que valid_from < valid_to ao criar/atualizar relações
