from fastapi import APIRouter

from auth.src.api.v1 import account_router, auth_router, history_router, role_router, social_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(
    auth_router, prefix='/auth', tags=['User Authentication']
)
main_router.include_router(
    history_router, prefix='/history', tags=['Login History']
)
main_router.include_router(
    role_router, prefix='/role', tags=['Roles']
)
main_router.include_router(
    account_router, prefix='/account', tags=['Account']
)
main_router.include_router(
    social_router, prefix='/social', tags=['Social Auth']
)
