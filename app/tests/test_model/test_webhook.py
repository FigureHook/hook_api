import pytest
from app.models import Webhook


@pytest.mark.usefixtures("db")
class TestWebhook:
    def test_token_encryption(self):
        token = "theverysecrettoken"
        w = Webhook(channel_id="123123", id="asdf", token=token, lang="ja")
        assert type(w.token) is str
        assert type(w.decrypted_token) is str
        assert w.decrypted_token == token
