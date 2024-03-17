from fastapi import APIRouter, Query
from starlette.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.services.yandex import YandexService, get_yandex_service
from auth.src.services.authentication import get_authentication_service, AuthenticationService
from auth.src.services.history import HistoryService, get_history_service
from auth.src.core.db import get_async_session
from auth.src.core.config import settings
from auth.src.core.constants import YANDEX_AUTH_URL


router = APIRouter()


@router.get("/login")
async def login_via_yandex():
    auth_url = YANDEX_AUTH_URL + settings.yandex.client_id
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def yandex_callback(
        code: str = Query(...),
        yandex_service: YandexService = Depends(get_yandex_service),
        session: AsyncSession = Depends(get_async_session),
        auth_service: AuthenticationService = Depends(get_authentication_service),
        history_service: HistoryService = Depends(get_history_service)
):
    user_info = await yandex_service.get_user_info(code)
    social_id = user_info.get("id")
    login = user_info.get("default_email")

    user, is_new_user, random_password = await yandex_service.new(session=session, social_id=social_id, login=login)
    await history_service.create(session, user.id)

    role = await user.awaitable_attrs.role

    await auth_service.new_token_pair(subject=str(user.id), claims={'access_level': role.access_level})

    if is_new_user:
        return user.username, random_password

    return {'detail': 'Successfully login'}
