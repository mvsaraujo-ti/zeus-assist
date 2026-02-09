# app/core/text_normalizer.py

import unicodedata
import re


def normalize_text(text: str) -> str:
    """
    Normaliza texto para comparação determinística.

    Regras:
    - lowercase
    - remove acentos
    - remove pontuação leve
    - normaliza espaços
    """

    if not text:
        return ""

    # lowercase
    text = text.lower()

    # remove acentos
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        c for c in text if not unicodedata.combining(c)
    )

    # remove pontuação leve (mantém letras e números)
    text = re.sub(r"[^\w\s]", " ", text)

    # normaliza espaços
    text = re.sub(r"\s+", " ", text).strip()

    return text
