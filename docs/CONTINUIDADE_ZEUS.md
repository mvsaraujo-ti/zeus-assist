📘 CONTINUIDADE TÉCNICA — PROJETO ZEUS
Visão Geral

ZEUS é um assistente institucional de TI, com foco em:

Respostas previsíveis

Fonte da verdade controlada

Arquitetura simples, auditável e evolutiva

O projeto NÃO é um chatbot genérico.

Princípios Fundamentais (NÃO QUEBRAR)

YAML é a fonte da verdade

Rotas nunca acessam YAML diretamente

IA não decide respostas

IA apenas formata texto

Alterou YAML → reiniciar backend

Separação clara de responsabilidades

Estrutura Oficial do Projeto
zeus/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       └── ask.py
│   ├── services/
│   │   ├── vault_service.py
│   │   └── ai_service.py
│   ├── providers/
│   │   └── ollama_client.py
│   ├── core/
│   │   └── guardrails.py
│   ├── schemas/
│   │   └── ask.py
│   ├── config/
│   │   └── settings.py
│   └── vault/
│       ├── flows.yaml
│       ├── systems.yaml
│       └── contacts.yaml
├── frontend/
│   ├── index.html
│   └── app.js
├── docs/
│   └── CONTINUIDADE_ZEUS.md
├── .env
├── .gitignore
├── README.md
└── requirements.txt

Função de Cada Pasta / Arquivo
app/main.py

Ponto de entrada da aplicação FastAPI

Registra rotas

NÃO contém lógica de negócio

app/api/v1/ask.py

Endpoint principal (/ask)

Recebe a pergunta do usuário

Fluxo correto:

Chama guardrails

Se não houver resposta fixa → chama vault_service

Recebe resultado estruturado

Chama IA apenas para formatação (se habilitada)

❌ Nunca acessar YAML
❌ Nunca decidir resposta

app/core/guardrails.py

Regras institucionais

Respostas fixas (quem é o Zeus, o que faz, etc.)

Bloqueia perguntas fora do escopo

Executado antes da busca no Vault

app/services/vault_service.py

ÚNICO local que acessa arquivos YAML

Responsável por:

Ler YAML

Normalizar dados

Aplicar lógica de busca

Calcular score

Futuro: busca unificada

app/services/ai_service.py

Integração com IA

IA:

Recebe texto pronto

Apenas melhora legibilidade

Controlada por feature toggle (ZEUS_AI_ENABLED)

app/providers/ollama_client.py

Cliente isolado para Ollama

Timeout curto

Fail-safe ativo

Nunca chamado diretamente pela rota

app/schemas/ask.py

Schemas Pydantic

Validação de entrada e saída

Evita respostas soltas

app/config/settings.py

Centraliza leitura de variáveis de ambiente

Nenhuma variável deve ser lida direto do os.environ fora daqui

app/vault/*.yaml

Fonte da verdade

Conteúdo institucional

Sem lógica

Estrutura simples e previsível

frontend/

Interface simples

HTML + JS puro

Apenas consome API

Sem lógica de negócio

Variáveis de Ambiente

Arquivo .env:

ZEUS_AI_ENABLED=true | false


true: IA formata resposta

false: resposta vem crua do backend

Como Subir o Backend
source venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m uvicorn app.main:app --reload

Fluxo Completo da Pergunta
Frontend
   ↓
/ask (API)
   ↓
guardrails.py
   ↓
vault_service.py
   ↓
(score + resultado)
   ↓
ai_service.py (opcional)
   ↓
Resposta final

Evoluções Planejadas (ordem correta)

Respostas institucionais (guardrails)

Busca unificada (flows + systems + contacts)

Logs e métricas

Cache por pergunta

Admin para gerar YAML

Autenticação (futuro)

Erros Comuns a Evitar

Acessar YAML direto na rota

Criar lógica em main.py

Usar IA para decidir conteúdo

Ignorar __init__.py

Copiar projeto via ZIP sem versionamento

Estado Atual

Backend funcional

Frontend funcional

Vault definido

GitHub configurado

Arquitetura estável

Observação Final

O ZEUS foi desenhado para:

Crescer sem quebrar

Ser auditável

Ser entendido mesmo fora do contexto do chat
