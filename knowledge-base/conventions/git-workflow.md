# Git Workflow — CrystalClear

## Branching Strategy

Trunk-based development simplificado:

```
main (protected)
  └── feature/US01-user-registration
  └── feature/US06-submit-declaration
  └── fix/declaration-date-validation
```

- `main` é a branch protegida — só recebe merges via PR
- Cada user story ou fix tem a sua branch
- Branches são curtas (dias, não semanas)
- Após merge, a branch é eliminada

## Naming

### Branches
```
feature/US<número>-<descrição-curta>
fix/<descrição-curta>
refactor/<descrição-curta>
test/<descrição-curta>
docs/<descrição-curta>
```

### Commits
Conventional Commits:
```
<type>(<scope>): <description>

type: feat | fix | test | refactor | docs | chore
scope: auth | declarations | entities | analysis | graph | complaints | frontend | infra
```

Exemplos:
- `feat(auth): implement JWT login endpoint`
- `test(declarations): add validation tests for submit`
- `fix(graph): correct temporal filter for active relations`
- `refactor(services): extract base repository interface`
- `docs(api): update declaration endpoint contracts`

## Fluxo por tarefa (com agentes)

1. Branch criada a partir de `main`: `feature/US06-submit-declaration`
2. Agente X escreve testes → commit: `test(declarations): add submit declaration tests`
3. Developer valida testes
4. Agente Y implementa → commits incrementais: `feat(declarations): add declaration model`, `feat(declarations): implement submit service`
5. Agente Z faz review → comentários na PR
6. Developer faz validação final e merge

## Regras

- Nunca commit diretamente em `main`
- Nunca force push em branches partilhadas
- Cada commit deve deixar os testes a passar (green)
- Commits devem ser atómicos — uma mudança lógica por commit
- Messages em inglês
