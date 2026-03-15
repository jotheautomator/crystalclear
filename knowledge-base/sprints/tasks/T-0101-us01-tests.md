# Task Briefing — T-0101

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

**Testes** — Escrever testes com base nos critérios de aceitação.

## Agente atribuído

- **Executor:** Atlas
- **Reviewer (na fase seguinte):** Cipher

## Contexto da knowledge base

Ficheiros que DEVES consultar antes de começar:

- `architecture/system-overview.md` — arquitetura geral do sistema
- `architecture/api-contracts.md` — secção Auth (POST /auth/register)
- `architecture/data-model.md` — secção PostgreSQL, tabela `users`
- `conventions/code-style.md` — convenções Python
- `conventions/testing-strategy.md` — estratégia de testes, naming, Arrange-Act-Assert
- `conventions/naming-conventions.md` — naming de ficheiros e funções de teste
- `domain/glossary.md` — roles e seus significados

## Scope

### Ficheiros a criar

- `backend/tests/unit/test_auth_service.py` — testes da lógica de negócio de registo
- `backend/tests/unit/test_user_schemas.py` — testes de validação dos schemas Pydantic (password, email, role)

### Ficheiros que NÃO devem ser alterados

- `backend/app/core/*` — já existe e está funcional
- `backend/tests/conftest.py` — já existe, podes estendê-lo se necessário criando fixtures adicionais

## Dependências

Nenhuma — esta é a primeira tarefa do Sprint 1.

## Instruções específicas

### Para `test_user_schemas.py`

Testar a validação Pydantic dos schemas de registo. Os schemas ainda não existem — os testes definem o contrato esperado.

Testes a incluir:
1. **Schema válido**: email válido, password forte, role permitido → aceite
2. **Email inválido**: formato incorreto → rejeição com erro
3. **Password fraca — sem maiúscula**: → rejeição
4. **Password fraca — sem minúscula**: → rejeição
5. **Password fraca — sem dígito**: → rejeição
6. **Password fraca — sem caractere especial**: → rejeição
7. **Password fraca — menos de 8 chars**: → rejeição
8. **Role inválido — ADMIN**: → rejeição (não permitido no auto-registo)
9. **Role inválido — string aleatória**: → rejeição
10. **Cada role válido**: POLITICAL_AGENT, CITIZEN, JOURNALIST, ETHICS_COMMITTEE → aceite

### Para `test_auth_service.py`

Testar a lógica de negócio do AuthService. O service ainda não existe — os testes definem o comportamento esperado.

Testes a incluir:
1. **Registo com sucesso**: dados válidos → retorna user com status PENDING, sem password no retorno
2. **Email duplicado**: email já existe → raise DuplicateError
3. **Password é hashed**: após registo, password_hash não é igual à password original
4. **Password é verificável**: hash gerado é compatível com verify_password
5. **Status PENDING**: user criado tem status PENDING
6. **person_node_id é None**: no registo, person_node_id deve ser None (só é preenchido na aprovação)

Usar mocks para o UserRepository — o repositório ainda não existe, mas a interface deve ser mockada.

### Padrão esperado dos testes

```python
# Naming: test_<contexto>_<ação>_<resultado>
# Estrutura: Arrange-Act-Assert
# Mocks: unittest.mock ou pytest-mock para repositórios

import pytest
from unittest.mock import AsyncMock, MagicMock

class TestUserSchemaValidation:
    def test_register_schema_with_valid_data_accepts(self):
        # Arrange
        ...
        # Act
        ...
        # Assert
        ...

class TestAuthService:
    @pytest.fixture
    def mock_user_repo(self):
        repo = AsyncMock()
        repo.get_by_email = AsyncMock(return_value=None)
        repo.create = AsyncMock()
        return repo
```

## Restrições adicionais

- Não implementar o service nem os schemas — apenas os testes
- Os testes devem FALHAR quando corridos (red phase do TDD) — é esperado
- Usar imports que reflitam a estrutura de pastas definida na arquitetura:
  - `from app.schemas.user import UserRegisterRequest`
  - `from app.services.auth_service import AuthService`
  - `from app.core.exceptions import DuplicateError`
- Não criar testes de API/endpoint nesta task — apenas unit tests do service e schemas

## Definition of Done

- [ ] `test_user_schemas.py` cobre os 10 cenários de validação listados
- [ ] `test_auth_service.py` cobre os 6 cenários de lógica de negócio listados
- [ ] Todos os testes seguem naming convention: `test_<contexto>_<ação>_<resultado>`
- [ ] Todos os testes seguem padrão Arrange-Act-Assert
- [ ] Testes são independentes entre si (sem estado partilhado)
- [ ] Imports apontam para os módulos corretos (mesmo que não existam ainda)
- [ ] Código segue as convenções em `conventions/code-style.md`
