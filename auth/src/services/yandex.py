from functools import lru_cache

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.models.social import SocialAccount
from auth.src.services.users import get_user_service
from auth.src.services.roles import get_role_service
from auth.src.services.authentication import get_authentication_service
from auth.src.utils.random_string import generate_random_string


class YandexService:
    social_name = 'Yandex'
    role_service = get_role_service()
    user_service = get_user_service()
    auth_service = get_authentication_service()

    async def get(self, session: AsyncSession, social_id) -> SocialAccount | None:
        return (await session.scalars(select(SocialAccount).where(
            and_(
                SocialAccount.social_id == social_id,
                SocialAccount.social_name == self.social_name
            )
        ))).first()

    async def new(self, session: AsyncSession, social_id: str, login: str):
        if social_acc := await self.get(session, social_id) is not None:
            return await self.user_service.get(session, social_acc.user_id)

        random_password = generate_random_string()
        default_role = await self.role_service.get_default_role(session)
        user = await self.user_service.create(
            session=session, username=login, password=random_password, role=default_role
        )

        social_acc = SocialAccount(
            user_id=user.id,
            social_id=social_id,
            social_name=self.social_name
        )

        session.add(social_acc)
        await session.commit()

        await self.auth_service.new_token_pair(subject=str(user.id), claims={'access_level': default_role.access_level})

        return login, random_password


@lru_cache
def get_yandex_service() -> YandexService:
    return YandexService()
