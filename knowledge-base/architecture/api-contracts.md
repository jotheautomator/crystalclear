# API Contracts — CrystalClear (Sprint 1)

## Base URL

```
/api/v1
```

## Autenticação

Todos os endpoints (exceto registro e login) requerem header:
```
Authorization: Bearer <access_token>
```

## Roles e Permissões

| Endpoint group    | ADMIN | POLITICAL_AGENT | ETHICS_COMMITTEE | JOURNALIST | CITIZEN |
|-------------------|-------|-----------------|------------------|------------|---------|
| Registration mgmt | ✅    | ❌             | ❌               | ❌        | ❌      |
| Institutions CRUD | ✅    | read            | read             | read       | read    |
| Functions CRUD    | ✅    | read            | read             | read       | read    |
| Declarations      | ❌    | own             | validate         | ❌         | ❌     |
| Analysis          | ❌    | own             | ✅               | filtered   | filtered|
| Complaints        | ❌    | ❌             | ✅               | ❌         | create  |

---

## 1. Auth

### POST /auth/register
Solicitar registo na plataforma (US01).

Request:
```json
{
    "email": "string",
    "password": "string",
    "full_name": "string",
    "requested_role": "political_agent | citizen | journalist | ethics_committee"
}
```

Response (201):
```json
{
    "id": "uuid",
    "email": "string",
    "full_name": "string",
    "requested_role": "string",
    "status": "pending",
    "created_at": "datetime"
}
```

### POST /auth/login

Request:
```json
{
    "email": "string",
    "password": "string"
}
```

Response (200):
```json
{
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer",
    "user": {
        "id": "uuid",
        "email": "string",
        "full_name": "string",
        "role": "string"
    }
}
```

### POST /auth/refresh

Request:
```json
{
    "refresh_token": "string"
}
```

---

## 2. Registration Management (US02)

### GET /admin/registrations?status=pending
Lista pedidos de registo.

Response (200):
```json
{
    "items": [
        {
            "id": "uuid",
            "email": "string",
            "full_name": "string",
            "requested_role": "string",
            "status": "pending",
            "created_at": "datetime"
        }
    ],
    "total": 0
}
```

### PATCH /admin/registrations/{id}
Aprovar ou rejeitar pedido (US02).

Request:
```json
{
    "action": "approve | reject",
    "rejection_reason": "string (optional)"
}
```

---

## 3. Institutions (US03, US04)

### GET /institutions?type={type}&sort=name
Listar instituições, agrupadas por tipo (US03).

Response (200):
```json
{
    "groups": [
        {
            "type": "company",
            "institutions": [
                {
                    "id": "uuid",
                    "name": "string",
                    "type": "string"
                }
            ]
        }
    ]
}
```

### POST /institutions
Registar instituição (US04). Requer role ADMIN.

Request:
```json
{
    "name": "string",
    "type": "company | party | foundation | institute | association | public_body"
}
```

---

## 4. Functions (US05)

### GET /functions
Listar funções disponíveis.

### POST /functions
Registar função. Requer role ADMIN.

Request:
```json
{
    "title": "string",
    "description": "string (optional)"
}
```

---

## 5. Declarations (US06, US07, US08)

### POST /declarations
Submeter declaração de interesses (US06). Requer role POLITICAL_AGENT.

Request:
```json
{
    "type": "initial | regular | exceptional",
    "reference_date": "date",
    "positions": [
        {
            "institution_name": "string",
            "institution_type": "string",
            "function_title": "string",
            "nature": "public | private | social",
            "payment": 0.0,
            "start_date": "date",
            "end_date": "date | null"
        }
    ],
    "assets": [
        {
            "asset_type": "urban_real_estate | rural_real_estate",
            "description": "string",
            "estimated_value": 0.0,
            "acquisition_date": "date | null"
        }
    ],
    "participations": [
        {
            "institution_name": "string",
            "participation_type": "quotas | shares | holdings",
            "market_value": 0.0,
            "percentage": 0.0
        }
    ],
    "supports": [
        {
            "institution_name": "string",
            "institution_type": "string",
            "amount": 0.0,
            "description": "string"
        }
    ]
}
```

### GET /declarations/{id}
Consultar declaração (US07). Filtra dados sensíveis por role.

### GET /declarations?agent_id={id}&status={status}
Listar declarações de um agente.

### PATCH /declarations/{id}/validate
Validar ou rejeitar declaração (US08). Requer role ETHICS_COMMITTEE.

Request:
```json
{
    "action": "validate | reject",
    "reviews": [
        {
            "section": "positions | assets | participations | supports",
            "item_id": "uuid (optional)",
            "comment": "string"
        }
    ]
}
```

---

## 6. Analysis (US09, US10, US11)

### GET /analysis/agents/{id}/situation?date={date}
Situação integrada de um agente numa data (US09). Requer ETHICS_COMMITTEE.

Response (200):
```json
{
    "agent": {
        "id": "uuid",
        "name": "string"
    },
    "date": "date",
    "positions": [...],
    "assets": [...],
    "participations": [...],
    "supports": [...],
    "network": {
        "nodes": [...],
        "edges": [...]
    }
}
```

### GET /analysis/agents/{id}/income?start_date={date}&end_date={date}
Evolução de rendimento (US10). Requer JOURNALIST.

Response (200):
```json
{
    "agent": {
        "id": "uuid",
        "name": "string"
    },
    "period": {
        "start": "date",
        "end": "date"
    },
    "income_timeline": [
        {
            "date": "date",
            "total_income": 0.0,
            "sources": [
                {
                    "institution": "string",
                    "function": "string",
                    "payment": 0.0
                }
            ]
        }
    ]
}
```

### GET /analysis/agents/{id}/assets?date={date}
Património numa data (US11). Dados filtrados por role.

Response (200):
```json
{
    "agent": {
        "id": "uuid",
        "name": "string"
    },
    "date": "date",
    "assets": [
        {
            "type": "string",
            "description": "string",
            "estimated_value": 0.0
        }
    ],
    "total_estimated_value": 0.0
}
```

---

## 7. Complaints (US12)

### POST /complaints
Submeter queixa (US12). Requer role CITIZEN.

Request:
```json
{
    "political_agent_id": "uuid",
    "agent_role": "string",
    "reference_date": "date",
    "description": "string"
}
```

---

## Convenções de Resposta

### Sucesso
- 200 OK (leitura)
- 201 Created (criação)
- 204 No Content (delete)

### Erros
```json
{
    "detail": {
        "code": "string",
        "message": "string",
        "field": "string (optional)"
    }
}
```

- 400 Bad Request (validação)
- 401 Unauthorized (sem token)
- 403 Forbidden (role insuficiente)
- 404 Not Found
- 409 Conflict (duplicado)
- 422 Unprocessable Entity (Pydantic validation)
