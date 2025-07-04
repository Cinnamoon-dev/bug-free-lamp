from fastapi import APIRouter
from src.services.userTypeService import UserTypeService
from src.schemas.userTypeSchema import UserTypeSchema

router = APIRouter(prefix="/user/type", tags=["user type"])

@router.get("/all")
def user_type_all():
    data = UserTypeService().get_all()
    return {"data": data}

@router.get("/view/{user_type_id:int}")
def user_type_view(user_type_id: int):
    return

@router.post("/add")
def user_type_add(user_type: UserTypeSchema):
    response = UserTypeService().add(user_type)
    return response

@router.put("/edit/{user_type_id:int}")
def user_type_edit(user_type_id: int):
    return

@router.delete("/delete/{user_type_id:int}")
def user_type_delete(user_type_id: int):
    return