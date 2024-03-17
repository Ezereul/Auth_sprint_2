from enum import IntEnum

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
