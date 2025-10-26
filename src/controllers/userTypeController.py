from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request

from ._helpers import PermissionChecker
from src.infra.database import PgDatabase
from src.schemas.userTypeSchema import UserTypeSchema
from src.services.userTypeService import UserTypeService

router = APIRouter(prefix="/user/type", tags=["user type"])


@router.get("/")
def user_type_all(
    request: Request,
    page: int = 1,
    rows_per_page: int = 10,
    sort_by: str | None = None,
    perms=Depends(PermissionChecker("tipo_usuario-all")),
):
    return UserTypeService(PgDatabase()).all(request.query_params)


@router.get("/{user_type_id:int}")
def user_type_view(
    user_type_id: int, perms=Depends(PermissionChecker("tipo_usuario-view"))
):
    user_type = UserTypeService(PgDatabase()).view(user_type_id)

    if user_type is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": True,
                "message": f"User type with id {user_type_id} not found",
            },
        )

    return JSONResponse(status_code=200, content={"error": False, "data": user_type})


@router.post("/")
def user_type_add(
    user_type: UserTypeSchema, perms=Depends(PermissionChecker("tipo_usuario-add"))
):
    inserted_id = UserTypeService(PgDatabase()).add(user_type)
    return JSONResponse(
        status_code=200,
        content={
            "error": False,
            "message": f"User type inserted successfully",
            "id": inserted_id,
        },
    )


@router.put("/{user_type_id:int}")
def user_type_edit(
    user_type_id: int,
    user_type: UserTypeSchema,
    perms=Depends(PermissionChecker("tipo_usuario-edit")),
):
    UserTypeService(PgDatabase()).edit(user_type_id, user_type)
    return JSONResponse(
        status_code=200,
        content={"error": False, "message": "User type edited successfully"},
    )


@router.delete("/{user_type_id:int}")
def user_type_delete(
    user_type_id: int, perms=Depends(PermissionChecker("tipo_usuario-delete"))
):
    UserTypeService(PgDatabase()).delete(user_type_id)
    return JSONResponse(
        status_code=200,
        content={"error": False, "message": "User type deleted successfully"},
    )
