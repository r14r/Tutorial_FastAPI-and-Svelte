from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator


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

    @field_validator("password")
    @classmethod
    def password_must_fit_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes when encoded as UTF-8")
        return value


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


class OllamaMessage(BaseModel):
    role: str
    content: str


class OllamaBaseRequest(BaseModel):
    model: str
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[str | int] = None

    model_config = ConfigDict(extra="allow")


class OllamaChatRequest(OllamaBaseRequest):
    messages: List[OllamaMessage]
    format: Optional[str] = None
    stream: bool = False


class OllamaGenerateRequest(OllamaBaseRequest):
    prompt: Optional[str] = None
    input: Optional[str] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    stream: bool = False


class OllamaPullRequest(BaseModel):
    model: str
    insecure: Optional[bool] = None
    stream: bool = True
