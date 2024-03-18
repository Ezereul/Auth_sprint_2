from functools import lru_cache

import httpx
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.core.config import settings
from auth.src.core.constants import YANDEX_TOKEN_URL, YANDEX_USER_INFO_URL
from auth.src.models.social import SocialAccount
from auth.src.services.roles import get_role_service
from auth.src.services.users import get_user_service
from auth.src.utils.random_string import generate_random_string


class YandexService:
    social_name = 'Yandex'
    role_service = get_role_service()
    user_service = get_user_service()

    async def get(self, session: AsyncSession, social_id) -> SocialAccount | None:
        return (await session.scalars(select(SocialAccount).where(
            and_(
                SocialAccount.social_id == social_id,
                SocialAccount.social_name == self.social_name
            )
        ))).first()

    async def create(self, session: AsyncSession, user_id: str, social_id: str):
        social_acc = SocialAccount(
            user_id=user_id,
            social_id=social_id,
            social_name=self.social_name
        )

        session.add(social_acc)
        await session.commit()

    async def new(self, session: AsyncSession, social_id: str, login: str):
        if (social_acc := await self.get(session, social_id)) is not None:
            return await social_acc.awaitable_attrs.user, False, None

        if (user := await self.user_service.get_by_name(session, login)) is not None:
            await self.create(session, user.id, social_id)
            return user, False, None

        random_password = generate_random_string()
        default_role = await self.role_service.get_default_role(session)

        user = await self.user_service.create(
            session=session, username=login, password=random_password, role=default_role
        )

        await self.create(session, user.id, social_id)

        return user, True, random_password

    async def get_user_info(self, code):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.yandex.client_id,
            "client_secret": settings.yandex.client_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(YANDEX_TOKEN_URL, headers=headers, data=data)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="OAuth token exchange failed")
            tokens = response.json()
            access_token = tokens.get("access_token")

            user_info_response = await client.get(
                YANDEX_USER_INFO_URL, headers={"Authorization": "OAuth " + access_token}
            )

        return user_info_response.json()


@lru_cache
def get_yandex_service() -> YandexService:
    return YandexService()
