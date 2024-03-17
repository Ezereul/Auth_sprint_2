from http import HTTPStatus

from fastapi import HTTPException
from fastapi_pagination.api import AbstractParams, resolve_params


def check_params() -> AbstractParams:
    params = resolve_params()

    if params.page * params.size > 10000:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Amount of entries > 10k is not supported. '
                   'Please try to apply filters/use search endpoint.'
        )
    return params
