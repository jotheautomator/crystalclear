# Testing Strategy — CrystalClear

## Filosofia

Seguimos TDD (Test-Driven Development) com cross-check entre agentes. Os testes são a especificação executável do sistema — escritos antes da implementação, por um agente diferente do que implementa.

## Pirâmide de Testes

```
         ╱╲
        ╱ E2E ╲          Poucos, lentos, alto valor
       ╱────────╲
      ╱Integration╲      Moderados, testam contratos
     ╱──────────────╲
    ╱   Unit Tests    ╲   Muitos, rápidos, isolados
   ╱────────────────────╲
```

### Unit Tests
- Testam uma unidade (função, método, classe) isoladamente
- Dependências externas são mocked
- Devem ser rápidos (< 100ms cada)
- Cobertura alvo: > 80% em services e domain models

### Integration Tests
- Testam a interação entre camadas (API → Service → Repository)
- Usam base de dados de teste real (PostgreSQL e Neo4j em Docker)
- Testam contratos da API (request/response)
- Testam autorização por role

### E2E Tests (Sprint 2+)
- Testam fluxos completos do utilizador
- Frontend + Backend integrados

## Framework e Ferramentas

### Backend (Python)
- **pytest** como runner
- **pytest-asyncio** para testes async
- **pytest-cov** para cobertura
- **httpx** (AsyncClient) para testar endpoints FastAPI
- **factory-boy** para gerar dados de teste
- **testcontainers** para PostgreSQL e Neo4j de teste

### Frontend (TypeScript)
- **Vitest** como runner
- **Testing Library** para componentes React
- **MSW (Mock Service Worker)** para mockar API calls

## Convenções de Naming

### Ficheiros de teste
- Backend: `test_<módulo>.py` dentro de `tests/unit/` ou `tests/integration/`
- Frontend: `<Component>.test.tsx` junto ao componente

### Nomes de testes
Padrão: `test_<contexto>_<ação>_<resultado_esperado>`

```python
# Bom
def test_login_with_valid_credentials_returns_token():
def test_login_with_wrong_password_returns_401():
def test_submit_declaration_without_positions_raises_validation_error():
def test_get_agent_situation_on_date_returns_active_positions_only():

# Mau
def test_login():
def test_error():
def test_declaration():
```

## Estrutura de um Teste

Seguir o padrão **Arrange → Act → Assert**:

```python
def test_validate_declaration_marks_as_validated():
    # Arrange
    declaration = DeclarationFactory(status="submitted")
    reviewer = UserFactory(role="ethics_committee")

    # Act
    result = declaration_service.validate(
        declaration_id=declaration.id,
        reviewer_id=reviewer.id,
        reviews=[],
    )

    # Assert
    assert result.status == "validated"
    assert result.validated_by == reviewer.id
    assert result.validated_at is not None
```

## O Que Testar por Camada

### Domain Models
- Validações e invariantes de negócio
- Comportamento de métodos
- Edge cases (valores nulos, limites)

### Services
- Lógica de negócio
- Orquestração entre repositórios
- Error handling (not found, forbidden, conflict)
- Regras de autorização

### API Layer
- Serialização/deserialização (Pydantic)
- Status codes corretos
- Autorização por role
- Validação de input

### Repositories
- Queries funcionam corretamente (integration tests)
- Edge cases (empty results, large datasets)

### Graph (Neo4j)
- Queries temporais retornam dados corretos para uma data
- Sincronização PostgreSQL → Neo4j funciona
- Métricas de rede (centralidade, etc.) calculadas corretamente

## Fixtures Partilhadas

Definidas em `tests/conftest.py`:

```python
@pytest.fixture
def test_db():
    """Provide a clean test database session."""

@pytest.fixture
def test_client(test_db):
    """Provide a test HTTP client with database."""

@pytest.fixture
def admin_token(test_client):
    """Provide an authenticated admin token."""

@pytest.fixture
def political_agent_token(test_client):
    """Provide an authenticated political agent token."""

@pytest.fixture
def sample_declaration(test_db):
    """Provide a sample submitted declaration."""
```

## Regras

1. **Testes primeiro, implementação depois** — o agente que escreve testes entrega antes do agente que implementa começar
2. **Testes independentes** — cada teste funciona isoladamente, sem depender de ordem de execução
3. **Testes determinísticos** — sem dependências de tempo real, random sem seed, ou estado externo
4. **Um assert por conceito** — cada teste verifica uma coisa; vários asserts permitidos se testam o mesmo conceito
5. **Não testar implementação** — testar comportamento, não detalhes internos
6. **Mocks com parcimónia** — preferir integration tests com DB real quando possível
