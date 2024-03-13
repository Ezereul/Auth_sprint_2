from fastapi import APIRouter

from auth.src.api.v1 import account_router, auth_router, history_router, role_router

main_router = APIRouter()

main_router.include_router(
    auth_router, prefix='/api/v1/auth', tags=['User Authentication']
)
main_router.include_router(
    history_router, prefix='/api/v1/history', tags=['Login History']
)
main_router.include_router(
    role_router, prefix='/api/v1/role', tags=['Roles']
)
main_router.include_router(
    account_router, prefix='/api/v1/account', tags=['Account']
)
