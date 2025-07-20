from fastapi import APIRouter, Request


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
def user_add(user):
    return

@router.put("/{user_id:int}")
def user_edit(user_id: int, user):
    return

@router.delete("/{user_id:int}")
def user_delete(user_id: int):
    return