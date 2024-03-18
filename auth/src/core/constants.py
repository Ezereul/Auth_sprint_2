from enum import IntEnum

from auth.src.core.config import settings
from auth.src.services.providers import YandexProvider

MIN_PASSWORD_LENGTH = 8
MIN_USERNAME_LENGTH = 4

YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize?response_type=code&client_id="
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"

DEFAULT_ROLE_DATA = {
    'name': 'user',
    'access_level': 1
}

SUPERUSER_ROLE_DATA = {
    'name': 'superuser',
    'access_level': 20
}


class RoleAccess(IntEnum):
    USER = 1
    ADMIN = 10
    SUPERUSER = 20


OAUTH_PROVIDERS = {
    "yandex": YandexProvider(
        client_id=settings.yandex.client_id,
        auth_url=YANDEX_AUTH_URL,
        token_url=YANDEX_TOKEN_URL,
    ),
}
