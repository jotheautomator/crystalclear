# Task Briefing — T-0103

## User Story

**Como** futuro utilizador,
**quero** solicitar registo na plataforma com as permissões adequadas ao meu papel,
**para** poder aceder às funcionalidades correspondentes.

## Fase desta tarefa

**Review** — Rever o código implementado na T-0102 com a lente de Estatística.

## Agente atribuído

- **Reviewer:** Cipher
- **Testes escritos por:** Atlas (T-0101)
- **Implementação por:** Bolt (T-0102)

## Contexto da knowledge base

Ficheiros que DEVES consultar antes de começar:

- `agents/cross-check-workflow.md` — formato do review e regras
- `architecture/api-contracts.md` — secção Auth
- `architecture/data-model.md` — tabela `users`
- `conventions/code-style.md` — verificar aderência
- `conventions/naming-conventions.md` — verificar aderência
- `domain/glossary.md` — terminologia correcta

## Ficheiros a rever

- `backend/app/schemas/user.py`
- `backend/app/models/user.py`
- `backend/app/services/auth_service.py`
- `backend/app/repositories/interfaces/user_repository.py`
- `backend/app/repositories/postgres/user_repository.py`
- `backend/app/api/auth.py`
- Alterações em `backend/app/main.py`

## Checklist de review

### Geral (todas as lentes)
- [ ] Todos os testes de T-0101 passam
- [ ] `ruff check .` sem erros
- [ ] `ruff format --check .` sem diferenças
- [ ] Código segue naming conventions do projeto
- [ ] Imports organizados correctamente
- [ ] Docstrings presentes em classes e funções públicas
- [ ] Scope respeitado — nenhum ficheiro fora do scope foi alterado
- [ ] Testes de T-0101 não foram modificados

### Lente de Cipher (Estatística e Dados)
- [ ] **Validação de dados:** A validação de password é robusta? Cobre todos os edge cases?
- [ ] **Qualidade dos dados:** O email é normalizado (lowercase)? Há risco de duplicados por case?
- [ ] **Hashing:** O bcrypt está configurado com rounds suficientes? O hash é determinístico nos testes?
- [ ] **Dados sensíveis:** Password nunca exposta em responses, logs, ou stack traces?
- [ ] **Edge cases de dados:** Como se comporta com emails muito longos? Full names com caracteres especiais? Unicode?
- [ ] **Consistência:** Os tipos de dados no SQLAlchemy model correspondem ao schema PostgreSQL documentado?
- [ ] **UUID generation:** Os UUIDs são gerados correctamente? Há risco de colisão?

## Formato do output

Produzir o review no formato definido em `agents/cross-check-workflow.md`:

```markdown
## Review — T-0103 (US01)
**Reviewer:** Cipher
**Lente aplicada:** Estatística e Dados

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

## Restrições

- Não alterar código — apenas produzir o review
- Se encontrar bloqueantes, descrever claramente o problema e sugerir solução
- Ser construtivo — sugerir alternativas, não apenas apontar problemas

## Definition of Done

- [ ] Review completo com todos os pontos da checklist avaliados
- [ ] Formato de review respeitado
- [ ] Veredicto claro
