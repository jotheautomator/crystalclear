# Definition of Done — CrystalClear

## Para uma tarefa estar "Done":

### Código
- Todos os testes passam (unitários, integração)
- Sem warnings do linter
- Código segue as convenções documentadas em `conventions/`
- Sem TODO/FIXME por resolver (ou registados como issues separadas)

### Review
- Cross-check concluído por agente reviewer
- Todos os bloqueantes (❌) do review resolvidos
- Validação final aprovada pelo developer humano

### Integração
- Branch merged na branch principal sem conflitos
- Pipeline de CI passa com sucesso
- Nenhum teste pré-existente ficou a falhar

### Documentação
- Se nova API: contratos atualizados em `architecture/api-contracts.md`
- Se nova entidade: `domain/entity-definitions.md` atualizado
- Se decisão técnica relevante: novo ADR criado em `adr/`
- README atualizado se necessário
