from app.services.intent_renderer import detect_contact_field


def test_detect_phone_intent():
    assert detect_contact_field("telefone da informática") == "phone"


def test_detect_email_intent():
    assert detect_contact_field("email da dtic") == "email"


def test_no_intent():
    assert detect_contact_field("informações da dtic") is None
