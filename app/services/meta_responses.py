# app/services/meta_responses.py

def zeus_identity() -> str:
    """
    Resposta institucional para perguntas do tipo:
    - Quem é você?
    - O que é o ZEUS?
    - Para que você serve?
    """

    return (
        "Sou o **ZEUS**, assistente institucional de TI do Tribunal de Justiça do Maranhão (TJMA).\n\n"
        "Fui criado para ajudar servidores, magistrados e colaboradores com informações "
        "claras, confiáveis e padronizadas sobre **sistemas internos**, **fluxos de atendimento** "
        "e **contatos de suporte**.\n\n"
        "Meu objetivo é facilitar o acesso à informação correta, reduzir retrabalho "
        "e agilizar o atendimento de demandas recorrentes de TI.\n\n"
        "**Como posso te ajudar melhor:**\n"
        "- Faça perguntas diretas, como *“O que é o Sentinela?”* ou *“Telefone da Informática”*;\n"
        "- Pergunte sobre procedimentos, por exemplo *“Como resetar senha?”*;\n"
        "- Use termos simples, não precisa linguagem técnica.\n\n"
        "Atualmente, estou em **fase de testes e evolução contínua**, e minhas respostas "
        "são baseadas exclusivamente em informações institucionais previamente cadastradas.\n\n"
        "Se algo não estiver disponível, posso te orientar sobre como acionar o suporte responsável."
    )
