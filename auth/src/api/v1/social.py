from fastapi import APIRouter, HTTPException, Query
from starlette.responses import RedirectResponse
import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.services.yandex import YandexService, get_yandex_service
from auth.src.core.db import get_async_session


router = APIRouter()

CLIENT_ID = 'be6f1cb7d8e442e9bc7a06681c69159a'
CLIENT_SECRET = '51cc00c7cebe4e9da19182c9fc1f3489'

@router.get("/login")
async def login_via_yandex():
    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}"
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def yandex_callback(
        code: str = Query(...),
        yandex_service: YandexService = Depends(get_yandex_service),
        session: AsyncSession = Depends(get_async_session)
):
    token_url = "https://oauth.yandex.ru/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="OAuth token exchange failed")
    tokens = response.json()
    access_token = tokens.get("access_token")

    user_info_url = "https://login.yandex.ru/info"
    headers = {"Authorization": "OAuth " + access_token}
    async with httpx.AsyncClient() as client:
        response = await client.post(user_info_url, headers=headers)
    info = response.json()
    social_id = info.get("social_id")
    login = info.get("login")

    return await yandex_service.new(session=session, social_id=social_id, login=login)

    # Используйте access_token для запроса данных пользователя через API Яндекса и сохранения в вашей базе данных

