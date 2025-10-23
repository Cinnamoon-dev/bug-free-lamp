from typing import Optional
from pydantic import BaseModel, Field, EmailStr, model_validator


class UserAddSchema(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    senha: str = Field(..., min_length=1, max_length=200)
    tipo_usuario_id: int

    @model_validator(mode="after")
    def check_tipo_usuario_id(self):
        if self.tipo_usuario_id < 1:
            raise ValueError("tipo_usuario_id deve ser >= 1.")
        return self


class UserEditSchema(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    tipo_usuario_id: Optional[int] = None

    @model_validator(mode="after")
    def check_tipo_usuario_id(self):
        if self.tipo_usuario_id is not None:
            if self.tipo_usuario_id < 1:
                raise ValueError("tipo_usuario_id deve ser >= 1.")
        return self
