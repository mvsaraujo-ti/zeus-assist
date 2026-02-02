"""
Cliente para comunicação com a API do Gemini.
"""

import os
import requests


def ask_gemini(prompt: str, model: str) -> str:
    """
    Envia um prompt para o Gemini via API REST.

    :param prompt: Texto completo enviado ao modelo
    :param model: Nome do modelo Gemini
    :return: Resposta gerada pelo Gemini
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Erro: GEMINI_API_KEY não configurada."

    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return f"Erro Gemini API: {response.status_code} - {response.text}"

    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
