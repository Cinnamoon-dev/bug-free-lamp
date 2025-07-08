from fastapi import APIRouter
from src.services.userTypeService import UserTypeService
from src.schemas.userTypeSchema import UserTypeSchema

router = APIRouter(prefix="/user/type", tags=["user type"])

@router.get("/")
def user_type_all():
    data = UserTypeService().all()
    return {"error": False, "data": data}

@router.get("/{user_type_id:int}")
def user_type_view(user_type_id: int):
    response = UserTypeService().view(user_type_id)
    return response

@router.post("/")
def user_type_add(user_type: UserTypeSchema):
    response = UserTypeService().add(user_type)
    return response

@router.put("/{user_type_id:int}")
def user_type_edit(user_type_id: int, user_type: UserTypeSchema):
    response = UserTypeService().edit(user_type_id, user_type)
    return response

@router.delete("/{user_type_id:int}")
def user_type_delete(user_type_id: int):
    response = UserTypeService().delete(user_type_id)
    return response