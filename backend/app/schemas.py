from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    # bcrypt rejects passwords longer than 72 bytes, so enforce the limit early
    password: constr(max_length=72)


class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedItems(BaseModel):
    items: List[ItemRead]
    total: int
