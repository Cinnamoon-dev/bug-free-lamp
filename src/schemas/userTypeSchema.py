from pydantic import BaseModel, Field


class UserTypeSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=50)
