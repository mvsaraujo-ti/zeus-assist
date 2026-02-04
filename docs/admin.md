# ZEUS – Admin API

## Autenticação
- HTTP Basic Auth
- Usuário e senha definidos pelo administrador

## Endpoint base
POST /api/v1/admin/vault/{item_type}

## Tipos permitidos
- system
- flow
- contact

## Exemplo – System
```json
{
  "id": "pje",
  "name": "PJe",
  "keywords": ["pje"],
  "description": "Sistema judicial"
}


