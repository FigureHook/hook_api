import pytest
from app.models import Webhook


@pytest.mark.usefixtures("db")
class TestWebhook:
    def test_lang_validation(self):
        Webhook(channel_id="123357805", id="asdfasdf",
                token="asdfasdf", lang="en")
        with pytest.raises(AssertionError):
            Webhook(channel_id="12311357805",
                    id="asdfsasdf", token="asdfassdf", lang="fr")

    def test_token_encryption(self):
        token = "theverysecrettoken"
        w = Webhook(channel_id="123123", id="asdf",
                    token=token, lang="ja")
        assert type(w.token) is str
        assert type(w.decrypted_token) is str
        assert w.decrypted_token == token
