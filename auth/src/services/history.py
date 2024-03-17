from datetime import datetime
import uuid
from datetime import datetime
from functools import lru_cache

from dateutil.relativedelta import relativedelta
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.models.history import LoginHistory
from auth.src.schemas.requests import PageParams
from auth.src.schemas.responses import PagedResponseSchema
from auth.src.utils.paginate import paginate_statement


class HistoryService:
    async def create(self, session: AsyncSession, user_id: uuid):
        history = LoginHistory(user_id=user_id)
        session.add(history)
        await session.commit()
        await session.refresh(history)

    async def get_history_paginated(
        self, session: AsyncSession, user_id: uuid, page_params: PageParams, month: int = None, year: int = None
    ) -> (PagedResponseSchema, int):
        current_date = datetime.now()
        if not month:
            month = current_date.month
        if not year:
            year = current_date.year

        stmt = select(LoginHistory).where(LoginHistory.user_id == user_id)  # noqa

        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)

        stmt = stmt.where(LoginHistory.login_time >= start_date, LoginHistory.login_time < end_date)

        stmt = stmt.order_by(desc(LoginHistory.login_time))  # noqa

        paginated_stmt, pages_count = await paginate_statement(session, stmt, page_params)
        return (await session.scalars(paginated_stmt)).all(), pages_count


@lru_cache
def get_history_service() -> HistoryService:
    return HistoryService()
