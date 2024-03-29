from typing import TypeVar

from fastapi.exceptions import HTTPException
from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.src.schemas.requests import PageParams
from auth.src.schemas.responses import PagedResponseSchema

T = TypeVar("T")


async def count_records(session: AsyncSession, stmt: Select) -> int:
    """Return count of records matches to statement."""
    count_stmt = stmt.with_only_columns(func.count()).order_by(None)
    return (await session.scalars(count_stmt)).first()


async def paginate_statement(session: AsyncSession, stmt: Select, page_params: PageParams) -> (PagedResponseSchema[T], int):
    """
    Paginate query.

    :param session: A database session.
    :param stmt: A SELECT statement to paginate.
    :param page_params: A PageParams, containing parameters for page.
    """
    stmt_records_count = await count_records(session, stmt)
    if stmt_records_count == 0:
        raise HTTPException(status_code=404, detail='No data for the specified period')
    pages_count = (stmt_records_count - 1) // page_params.size + 1

    if page_params.page > pages_count:
        raise ValueError('Page number is greater than total count (%s > %s)' % (page_params.page, pages_count))

    paginated_stmt = stmt.offset((page_params.page - 1) * page_params.size).limit(page_params.size)
    return paginated_stmt, pages_count
