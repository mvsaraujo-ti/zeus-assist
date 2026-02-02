"""
Arquivo de configuração central do ZEUS.

Responsável por:
- Definir modo de execução (LOCAL ou GEMINI)
- Centralizar nomes de modelos
"""

# Modos possíveis: "LOCAL" ou "GEMINI"
AI_MODE = "LOCAL"

# Modelos
OLLAMA_MODEL = "llama3.2:3b"
GEMINI_MODEL = "models/gemini-2.5-flash"
