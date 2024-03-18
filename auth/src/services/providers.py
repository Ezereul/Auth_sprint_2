class OAuthProvider:
    def __init__(self, client_id: str, auth_url: str, token_url: str):
        self.client_id = client_id
        self.auth_url = auth_url
        self.token_url = token_url

    def get_auth_url(self):
        pass


class YandexProvider(OAuthProvider):
    def get_auth_url(self):
        return self.auth_url + self.client_id
