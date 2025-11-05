from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request

from ._helpers import PermissionChecker
from src.infra.database import PgDatabase
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
    perms=Depends(PermissionChecker("usuario-all")),
):
    return UserService(PgDatabase()).all(request.query_params)


@router.get("/{user_id:int}")
def user_view(
    request: Request,
    user_id: int,
    show_fk_id: int | None = 1,
    perms=Depends(PermissionChecker("usuario-view"))
):
    user = UserService(PgDatabase()).view_controller(user_id, request.query_params)

    if user is None:
        return JSONResponse(
            status_code=404,
            content={"error": True, "message": f"User with id {user_id} not found"},
        )

    return JSONResponse(status_code=200, content={"error": False, "data": user})


@router.post("/")
def user_add(user: UserAddSchema, perms=Depends(PermissionChecker("usuario-add"))):
    inserted_id = UserService(PgDatabase()).add(user)
    return JSONResponse(
        status_code=200,
        content={
            "error": False,
            "message": f"User inserted successfully",
            "id": inserted_id,
        },
    )


@router.put("/{user_id:int}")
def user_edit(
    user_id: int, user: UserEditSchema, perms=Depends(PermissionChecker("usuario-edit"))
):
    UserService(PgDatabase()).edit(user_id, user)
    return JSONResponse(
        status_code=200, content={"error": False, "message": "User edited successfully"}
    )


@router.delete("/{user_id:int}")
def user_delete(user_id: int, perms=Depends(PermissionChecker("usuario-delete"))):
    UserService(PgDatabase()).delete(user_id)
    return JSONResponse(
        status_code=200,
        content={"error": False, "message": "User deleted successfully"},
    )
