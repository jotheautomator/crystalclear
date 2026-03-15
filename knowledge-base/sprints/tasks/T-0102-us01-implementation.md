# Task Briefing — T-0102

## User Story

**Como** futuro utilizador,
**quero** solicitar registo na plataforma com as permissões adequadas ao meu papel,
**para** poder aceder às funcionalidades correspondentes.

## Critérios de aceitação

- [ ] CA1: O utilizador preenche email, password, nome completo e seleciona um role de uma lista predefinida (POLITICAL_AGENT, CITIZEN, JOURNALIST, ETHICS_COMMITTEE).
- [ ] CA2: O role ADMIN não está disponível para auto-registo.
- [ ] CA3: A password é validada: mínimo 8 caracteres, pelo menos uma maiúscula, uma minúscula, um dígito e um caractere especial.
- [ ] CA4: O email é validado quanto ao formato e unicidade.
- [ ] CA5: Após registo, o utilizador fica com status PENDING e não pode fazer login até ser aprovado.
- [ ] CA6: A password é armazenada com hash bcrypt, nunca em texto claro.
- [ ] CA7: O endpoint retorna 201 com os dados do utilizador (sem password) ou 400/409 com erro descritivo.

## Fase desta tarefa

**Implementação** — Implementar até todos os testes passarem.

## Agente atribuído

- **Executor:** Bolt
- **Testes escritos por:** Atlas (T-0101 — já concluída e validada)

## Contexto da knowledge base

Ficheiros que DEVES consultar antes de começar:

- `architecture/system-overview.md` — camadas da aplicação
- `architecture/api-contracts.md` — secção Auth (POST /auth/register)
- `architecture/data-model.md` — secção PostgreSQL, tabela `users`
- `architecture/tech-stack.md` — dependências e versões
- `conventions/code-style.md` — padrões Python, repository pattern, service layer
- `conventions/naming-conventions.md` — naming de classes, módulos, variáveis
- `domain/glossary.md` — roles, statuses

## Testes a satisfazer

Os testes estão em:
- `backend/tests/unit/test_auth_service.py`
- `backend/tests/unit/test_user_schemas.py`

Corre `pytest tests/unit/test_auth_service.py tests/unit/test_user_schemas.py -v` para verificar o progresso.

## Scope

### Ficheiros a criar

- `backend/app/schemas/user.py` — Pydantic models para register request/response
- `backend/app/models/user.py` — SQLAlchemy model para a tabela `users`
- `backend/app/services/auth_service.py` — lógica de negócio de registo
- `backend/app/repositories/interfaces/user_repository.py` — interface abstrata
- `backend/app/repositories/postgres/user_repository.py` — implementação PostgreSQL
- `backend/app/api/auth.py` — router FastAPI com endpoint POST /auth/register

### Ficheiros a modificar

- `backend/app/main.py` — registar o router de auth

### Ficheiros que NÃO devem ser alterados

- `backend/app/core/*` — já funcional, não modificar
- `backend/tests/*` — nunca alterar testes escritos por outro agente

## Instruções específicas

### Camada de schemas (`app/schemas/user.py`)

```python
# DTOs esperados:
# - UserRegisterRequest: email, password, full_name, role
#   - password: validação customizada (min 8, maiúscula, minúscula, dígito, especial)
#   - role: enum com POLITICAL_AGENT, CITIZEN, JOURNALIST, ETHICS_COMMITTEE (sem ADMIN)
# - UserResponse: id, email, full_name, role, status (sem password)
```

Usar Pydantic v2 validators (`@field_validator`). Definir um Enum para Role e para Status.

### Camada de modelo (`app/models/user.py`)

SQLAlchemy model mapeado para a tabela `users` definida em `architecture/data-model.md`. Usar `mapped_column` do SQLAlchemy 2.x. Herdar de `app.core.database.Base`.

### Camada de repositório

Interface abstrata em `app/repositories/interfaces/user_repository.py`:
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: ...) -> ...: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> ... | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> ... | None: ...
```

Implementação PostgreSQL em `app/repositories/postgres/user_repository.py` usando SQLAlchemy async session.

### Camada de service (`app/services/auth_service.py`)

```python
class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def register(self, data: UserRegisterRequest) -> UserResponse:
        # 1. Check email uniqueness → DuplicateError
        # 2. Hash password
        # 3. Create user with status PENDING, person_node_id=None
        # 4. Return UserResponse (without password)
```

Usar exceções de `app.core.exceptions` — nunca raise HTTPException no service.

### Camada de API (`app/api/auth.py`)

Router FastAPI. Apanhar exceções do service e converter para HTTP responses:
- `DuplicateError` → 409 Conflict
- `ValidationError` → 400 Bad Request
- Sucesso → 201 Created

### Registo do router em `app/main.py`

Descomentar/adicionar:
```python
from app.api import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
```

## Dependências

- T-0101 (testes) deve estar concluída e validada

## Restrições adicionais

- Seguir estritamente o repository pattern — o service nunca acede à BD diretamente
- Nunca expor password ou password_hash em responses
- Usar dependency injection do FastAPI (`Depends`) para injetar repositórios no service
- Manter commits atómicos: model → schema → repository → service → router

## Definition of Done

- [ ] Todos os testes de T-0101 passam (green)
- [ ] Nenhum teste pré-existente falha
- [ ] `ruff check .` sem erros
- [ ] `ruff format --check .` sem alterações
- [ ] Código segue as convenções do projeto
- [ ] Endpoint funcional: `POST /api/v1/auth/register` responde corretamente
- [ ] Password nunca visível em logs, responses ou BD
