import base64
import http
import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from requests import Response

from movies.constants import RoleAccess

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {'username': username, 'password': password}
        response: Response = requests.post(url, data=json.dumps(payload))
        if response.status_code != http.HTTPStatus.OK:
            return None

        token: str = response.cookies.get('access_token_cookie')
        encoded_payload = token.split('.')[1]
        data = json.loads(base64.b64decode(encoded_payload + '=='))
        user_data = {
            'username': data.get('sub')[:29],
            'id': data.get('sub'),
            'is_stuff': check_access_level(data.get('access_level'), RoleAccess.ADMIN),
            'is_active': True
        }

        try:
            user, created = User.objects.update_or_create(**user_data)
            user.save()
        except Exception as e:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def check_access_level(token_access_level: int, required_access_level: int) -> bool:
    return token_access_level >= required_access_level
