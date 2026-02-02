# ZEUS – Assistente de TI

ZEUS é um assistente técnico institucional para suporte de TI (N1/N2).

- YAML como fonte da verdade
- FastAPI no backend
- Frontend simples em HTML + JS
- IA opcional apenas para formatação

## Como rodar o backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export $(grep -v '^#' .env | xargs)
python -m uvicorn app.main:app --reload
