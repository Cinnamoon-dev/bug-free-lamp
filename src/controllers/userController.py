from fastapi import APIRouter, Depends, Request

from ._helpers import PermissionChecker
from src.services.userService import UserService
from src.schemas.userSchema import UserAddSchema, UserEditSchema


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def user_all(
    request: Request,
    page: int = 1,
    rows_per_page: int = 10,
    sort_by: str | None = None,
    show_fk_id: int | None = 1,
    perms = Depends(PermissionChecker("usuario-all"))
):
    return UserService().all(request.query_params)

@router.get("/{user_id:int}")
def user_view(
    user_id: int, 
    perms = Depends(PermissionChecker("usuario-view"))
):
    return UserService().view(user_id)

@router.post("/")
def user_add(
    user: UserAddSchema,
    perms = Depends(PermissionChecker("usuario-add"))
):
    return UserService().add(user)

@router.put("/{user_id:int}")
def user_edit(
    user_id: int, 
    user: UserEditSchema,
    perms = Depends(PermissionChecker("usuario-edit"))
):
    return UserService().edit(user_id, user)

@router.delete("/{user_id:int}")
def user_delete(
    user_id: int,
    perms = Depends(PermissionChecker("usuario-delete"))
):
    return UserService().delete(user_id)