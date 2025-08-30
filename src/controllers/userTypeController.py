from fastapi import APIRouter, Depends, Request

from ._helpers import PermissionChecker
from src.schemas.userTypeSchema import UserTypeSchema
from src.services.userTypeService import UserTypeService

router = APIRouter(prefix="/user/type", tags=["user type"])

@router.get("/")
def user_type_all(
    request: Request,
    page: int = 1,
    rows_per_page: int = 10,
    sort_by: str | None = None,
    perms = Depends(PermissionChecker("tipo_usuario-all"))
):
    return UserTypeService().all(request.query_params)

@router.get("/{user_type_id:int}")
def user_type_view(
    user_type_id: int,
    perms = Depends(PermissionChecker("tipo_usuario-view"))
):
    response = UserTypeService().view(user_type_id)
    return response

@router.post("/")
def user_type_add(
    user_type: UserTypeSchema,
    perms = Depends(PermissionChecker("tipo_usuario-add"))
):
    response = UserTypeService().add(user_type)
    return response

@router.put("/{user_type_id:int}")
def user_type_edit(
    user_type_id: int, 
    user_type: UserTypeSchema,
    perms = Depends(PermissionChecker("tipo_usuario-edit"))
):
    response = UserTypeService().edit(user_type_id, user_type)
    return response

@router.delete("/{user_type_id:int}")
def user_type_delete(
    user_type_id: int,
    perms = Depends(PermissionChecker("tipo_usuario-delete"))
):
    response = UserTypeService().delete(user_type_id)
    return response