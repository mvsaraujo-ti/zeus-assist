from app.services.system_renderer import render_system


def test_render_system_access():
    raw = {
        "name": "DigiDoc",
        "access": {
            "network": "Rede interna TJMA"
        }
    }

    response = render_system(raw, "como acessar o digidoc")
    assert "Rede interna TJMA" in response
