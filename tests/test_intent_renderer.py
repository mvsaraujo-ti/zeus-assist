from app.services.intent_renderer import render_contact
from app.services.system_renderer import render_system
from app.services.flow_renderer import render_flow


def test_contact_phone_intent():
    raw = {
        "name": "Divisão de Cadastro",
        "channels": {
            "phone": "1234",
            "ramal": "5678",
            "email": "x@tjma.jus.br",
        }
    }
    r = render_contact(raw, "qual o telefone da divisão?")
    assert "1234" in r
    assert "ramal" not in r.lower()


def test_system_access_intent():
    raw = {
        "name": "SENTINELA",
        "access": {"url": "http://sentinela", "login_required": True}
    }
    r = render_system(raw, "como acessar o sentinela?")
    assert "http://sentinela" in r


def test_flow_steps_intent():
    raw = {
        "title": "Reset de Senha",
        "steps": ["Acessar sistema", "Clicar em esqueci senha"]
    }
    r = render_flow(raw, "como fazer reset de senha?")
    assert "1." in r
