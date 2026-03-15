# Workflow de Cross-Check entre Agentes

## Princípio

Nenhum agente trabalha isolado. Cada tarefa passa por pelo menos dois agentes antes de chegar à validação humana. Isto garante diversidade de perspetiva e reduz erros.

## Os três agentes

| Agente  | Lente preferencial                  | Foco no review                                          |
|---------|-------------------------------------|---------------------------------------------------------|
| Atlas   | Engenharia de Software              | Arquitetura, padrões, SOLID, testabilidade, API design  |
| Bolt    | Programação Orientada a Objetos     | Modelação, encapsulamento, coesão, relações de domínio  |
| Cipher  | Estatística e Análise de Dados      | Correção algorítmica, qualidade de dados, eficiência    |

## Fluxo de uma tarefa

```
┌─────────────────────────────────────────────────────────┐
│ 1. Developer humano cria task briefing                  │
│    (user story + critérios de aceitação + scope)        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Agente X escreve testes                              │
│    (baseado nos critérios de aceitação)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Developer humano valida testes                       │
│    (checkpoint crítico — os testes estão corretos?)     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Agente Y implementa                                  │
│    (até todos os testes passarem)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Agente Z faz review                                  │
│    (aplica a sua lente + checklist geral)               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Developer humano faz validação final e merge         │
└─────────────────────────────────────────────────────────┘
```

## Matriz de rotação

Para garantir que todos os agentes exercitam todos os papéis e que nenhum par se repete excessivamente, segue-se uma rotação. O ciclo base é:

| Tarefa | Testes  | Implementação | Review  |
|--------|---------|---------------|---------|
| T1     | Atlas   | Bolt          | Cipher  |
| T2     | Bolt    | Cipher        | Atlas   |
| T3     | Cipher  | Atlas         | Bolt    |
| T4     | Atlas   | Cipher        | Bolt    |
| T5     | Bolt    | Atlas         | Cipher  |
| T6     | Cipher  | Bolt          | Atlas   |

Após T6, o ciclo repete. Esta rotação pode ser ajustada pelo developer humano conforme necessário, mas o princípio de nunca ter o mesmo agente a escrever testes e a implementar a mesma tarefa deve ser mantido.

## Regras do cross-check

### Regra 1 — Separação de responsabilidades
O agente que escreve os testes NUNCA é o mesmo que implementa na mesma tarefa. Isto evita viés de confirmação.

### Regra 2 — Review com lente
O agente reviewer aplica sempre a sua lente de especialização, mas também verifica a checklist geral:
- Os testes passam?
- O código segue as convenções?
- O scope foi respeitado?
- A Definition of Done está cumprida?

### Regra 3 — Feedback acionável
O review deve ser concreto. Em vez de "isto podia ser melhor", dizer "esta classe tem duas responsabilidades — sugiro extrair X para uma classe separada".

### Regra 4 — Bloqueantes vs. sugestões
O review distingue claramente entre:
- ❌ **Bloqueantes:** Devem ser corrigidos antes do merge
- ⚠️ **Sugestões:** Melhorias opcionais que podem ser feitas agora ou em tarefa futura

### Regra 5 — Resolução de conflitos
Se o agente implementador discorda do review, a decisão final é do developer humano.

## Formato do review

```markdown
## Review — [TASK-ID]
**Reviewer:** [Atlas / Bolt / Cipher]
**Lente aplicada:** [ES / POO / Estatística]

### ✅ Pontos positivos
- ...

### ⚠️ Sugestões
- ...

### ❌ Bloqueantes
- ...

### Veredicto
- [ ] Aprovado
- [ ] Aprovado com sugestões
- [ ] Requer alterações (bloqueantes identificados)
```

## Exceções

- **Hotfix urgente:** Em caso de necessidade, o developer humano pode saltar o cross-check e implementar diretamente. Deve documentar a razão.
- **Tarefa trivial:** Para alterações muito pequenas (typos, ajustes de config), o cross-check pode ser simplificado para apenas um reviewer, sem fase de testes separada.
