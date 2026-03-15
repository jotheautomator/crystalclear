# Code Style Conventions — CrystalClear

## Python (Backend)

### Geral
- Python 3.12+
- Formatter/Linter: Ruff (substitui black + isort + flake8)
- Type checker: mypy (strict mode)
- Line length: 88 characters (Ruff default)
- Quotes: double quotes para strings

### Naming
- Ficheiros e módulos: `snake_case.py`
- Classes: `PascalCase`
- Funções e métodos: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- Variáveis: `snake_case`
- Parâmetros de URL/query: `snake_case`

### Imports
- Ordenados por Ruff (stdlib → third-party → local)
- Imports absolutos sempre (não usar relative imports)

### Type hints
- Obrigatórios em todas as assinaturas de funções públicas
- Obrigatórios em variáveis de classe
- Usar `from __future__ import annotations` para forward references

### Docstrings
- Google style para todas as funções/classes públicas
- Incluir Args, Returns, Raises

```python
def validate_declaration(
    declaration_id: UUID,
    reviewer_id: UUID,
    reviews: list[ReviewCreate],
) -> Declaration:
    """Validate a submitted declaration of interests.

    Args:
        declaration_id: The declaration to validate.
        reviewer_id: The ethics committee member performing validation.
        reviews: List of review comments for specific sections/items.

    Returns:
        The updated declaration with validated status.

    Raises:
        NotFoundError: If the declaration does not exist.
        ForbiddenError: If the declaration is not in 'submitted' status.
    """
```

### FastAPI específico
- Routers em ficheiros separados por domínio
- Pydantic schemas separados dos SQLAlchemy models
- Dependency injection via `Depends()` para services e repos
- Status codes explícitos em todos os endpoints

## TypeScript (Frontend)

### Geral
- TypeScript strict mode
- Formatter: Prettier
- Linter: ESLint com config recomendada
- Semicolons: sim
- Quotes: single quotes

### Naming
- Ficheiros de componentes: `PascalCase.tsx`
- Ficheiros utilitários: `camelCase.ts`
- Componentes React: `PascalCase`
- Funções e variáveis: `camelCase`
- Types e Interfaces: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- CSS classes (Tailwind): utility classes diretas

### Componentes React
- Functional components apenas (sem class components)
- Props tipadas com interface
- Exportações named (não default), exceto páginas

```tsx
interface AgentSituationProps {
  agentId: string;
  date: string;
}

export function AgentSituation({ agentId, date }: AgentSituationProps) {
  // ...
}
```

### State management
- Estado local: `useState` / `useReducer`
- Estado partilhado: Zustand stores
- Estado do servidor: considerar React Query para caching

## Git

### Commits
- Conventional Commits: `type(scope): description`
- Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `ci`
- Scope: `auth`, `declarations`, `institutions`, `analysis`, `graph`, `ui`, `infra`
- Exemplos:
  - `feat(declarations): add submission endpoint`
  - `test(auth): add login validation tests`
  - `refactor(graph): extract temporal query builder`

### Branches
- `main` — produção, sempre estável
- `develop` — integração
- `feature/<task-id>-<short-description>` — uma feature por branch
- `fix/<task-id>-<short-description>` — correção
- Merge via PR com review obrigatório
