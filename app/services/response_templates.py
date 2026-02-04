"""
Templates institucionais de resposta — ZEUS
"""

INTRO_HELP = "Posso te ajudar com isso."
OUTRO_HELP = "Fico à disposição se precisar."

def wrap_response(content: str) -> str:
    return f"{INTRO_HELP}\n\n{content}\n\n{OUTRO_HELP}"
