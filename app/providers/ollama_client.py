# app/providers/ollama_client.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def format_answer_with_ollama(raw_answer: str) -> str:
    """
    Envia a resposta do vault para o Ollama apenas para FORMATAÇÃO,
    seguindo padrão institucional do TJMA.
    """

    system_prompt = (
        "Você é um assistente institucional do Tribunal de Justiça do Maranhão (TJMA), "
        "atuando exclusivamente no suporte técnico N1.\n\n"
        "Regras obrigatórias:\n"
        "- NÃO crie, invente ou complemente informações.\n"
        "- NÃO interprete normas ou leis.\n"
        "- NÃO responda questões jurídicas.\n"
        "- Apenas reescreva o texto fornecido.\n\n"
        "Estilo da resposta:\n"
        "- Linguagem formal e institucional.\n"
        "- Clareza e objetividade.\n"
        "- Tom respeitoso e profissional.\n"
        "- Utilize listas quando houver passos.\n"
    )

    user_prompt = (
        "Reescreva o texto abaixo mantendo exatamente o conteúdo, "
        "apenas ajustando a forma conforme as regras acima:\n\n"
        f"{raw_answer}"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}\n{user_prompt}",
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json().get("response", raw_answer)
    except Exception:
        # Fail-safe: retorna o texto original
        return raw_answer
