from fastapi import APIRouter, Request

from src.services.userService import UserService
from src.schemas.userSchema import UserAddSchema, UserEditSchema


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def user_all(
    request: Request,
    page: int = 1,
    rows_per_page: int = 10,
    sort_by: str | None = None,
    show_fk_id: int | None = 1
):
    return UserService().all(request.query_params)

@router.get("/{user_id:int}")
def user_view(user_id: int):
    return UserService().view(user_id)

@router.post("/")
def user_add(user: UserAddSchema):
    return UserService().add(user)

@router.put("/{user_id:int}")
def user_edit(user_id: int, user: UserEditSchema):
    return UserService().edit(user_id, user)

@router.delete("/{user_id:int}")
def user_delete(user_id: int):
    return UserService().delete(user_id)