from fastapi import APIRouter, Request

from src.services.userService import UserService
from src.schemas.userSchema import UserAddSchema, UserEditSchema


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def user_all(
    request: Request,
    page: int = 1,
    rows_per_page: int = 10,
    sort_by: str | None = None
):
    return

@router.get("/{user_id:int}")
def user_view(user_id: int):
    return

@router.post("/")
def user_add(user: UserAddSchema):
    return UserService().add(user)

@router.put("/{user_id:int}")
def user_edit(user_id: int, user: UserEditSchema):
    return

@router.delete("/{user_id:int}")
def user_delete(user_id: int):
    return