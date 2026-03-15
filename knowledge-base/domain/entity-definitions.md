# Entity Definitions — CrystalClear

## Entidades Principais

### PoliticalAgent (Agente Político)
Pessoa que exerce funções políticas e é obrigada a submeter declarações de interesses.

- Atributos: nome, email, role político atual
- Comportamento: submete declarações, tem posições em instituições, possui ativos, tem participações empresariais
- Invariantes:
  - Deve ter pelo menos uma declaração inicial ao iniciar mandato
  - Não pode submeter nova declaração enquanto anterior estiver pendente de validação
- Relações: HOLDS_POSITION→Institution, OWNS→Asset, HAS_PARTICIPATION→Institution, RECEIVES_SUPPORT→Institution

### Institution (Instituição)
Entidade organizacional com a qual agentes políticos se relacionam.

- Tipos: Company, Party, Foundation, Institute, Association, PublicBody
- Atributos: nome (único), tipo
- Invariantes:
  - Nome deve ser único dentro do sistema
  - Tipo deve pertencer à lista predefinida
- Relações: destino de HOLDS_POSITION, HAS_PARTICIPATION, RECEIVES_SUPPORT

### Declaration (Declaração de Interesses)
Documento formal submetido por um agente político, contendo a sua situação patrimonial e profissional.

- Tipos: Initial, Regular, Exceptional
- Estados: Draft → Submitted → Validated | Rejected
- Atributos: tipo, data de referência, estado, data de submissão, data de validação
- Composição: contém Positions, Assets, Participations, Supports
- Invariantes:
  - Só pode ser validada/rejeitada se estiver no estado Submitted
  - Só membros da Ethics Committee podem validar
  - Quando rejeitada, deve ter pelo menos um review comment

### Position (Cargo/Posição)
Função exercida por um agente numa instituição, declarada numa declaração de interesses.

- Atributos: instituição, tipo de instituição, título da função, natureza (public/private/social), pagamento, data início, data fim
- Invariantes:
  - Data de início obrigatória
  - Se data de fim existe, deve ser posterior à data de início
  - Pagamento pode ser nulo (funções não remuneradas)

### Asset (Ativo/Património)
Bem possuído por um agente político.

- Tipos: UrbanRealEstate, RuralRealEstate
- Atributos: tipo, descrição, valor estimado, data de aquisição
- Invariantes:
  - Valor estimado deve ser positivo
  - Tipo deve pertencer à lista predefinida

### BusinessParticipation (Participação Empresarial)
Quotas, ações ou participações detidas por um agente numa empresa.

- Tipos: Quotas, Shares, Holdings
- Atributos: instituição, tipo de participação, valor de mercado, percentagem
- Invariantes:
  - Valor de mercado deve ser positivo
  - Percentagem, se indicada, entre 0 e 100

### Support (Apoio/Subsídio)
Valor recebido por um agente de uma instituição.

- Atributos: instituição, tipo de instituição, montante, descrição
- Invariantes:
  - Montante deve ser positivo

### Complaint (Queixa/Denúncia)
Comunicação de um cidadão sobre comportamento de um agente político.

- Estados: Submitted → UnderReview → Resolved | Dismissed
- Atributos: agente político alvo, role do agente na data, data de referência, descrição
- Invariantes:
  - Apenas cidadãos podem submeter queixas
  - Data de referência obrigatória
  - Descrição não pode ser vazia

### Function (Função)
Tipo de função política ou profissional (dados de referência).

- Atributos: título (único), descrição
- Invariantes:
  - Título deve ser único

### User (Utilizador)
Qualquer pessoa registada na plataforma.

- Roles: Admin, PoliticalAgent, Citizen, Journalist, EthicsCommittee
- Atributos: email (único), password hash, nome completo, role, estado ativo
- Invariantes:
  - Email deve ser único
  - Password deve ter pelo menos 7 caracteres alfanuméricos, incluindo 3 maiúsculas e 2 dígitos
  - Role deve pertencer à lista predefinida

### RegistrationRequest (Pedido de Registo)
Solicitação de registo na plataforma, pendente de aprovação.

- Estados: Pending → Approved | Rejected
- Atributos: email, nome, role solicitado, estado, razão de rejeição
- Invariantes:
  - Só Admins podem aprovar/rejeitar
  - Se rejeitado, deve ter razão de rejeição
