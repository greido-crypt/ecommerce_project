from typing import Optional, List, Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int
    errors: List[str] = []
    content: Optional[Any] = None


class TokenContent(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenResponse(BaseResponse):
    content: TokenContent


# Ответ для профиля пользователя
class ProfileContent(BaseModel):
    id: int
    username: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    icon: Optional[str]
    is_banned: bool
    is_deleted: bool
    role: str


class ProfileResponse(BaseResponse):
    content: ProfileContent


class ProfileListResponse(BaseResponse):
    content: List[ProfileContent]


# Ответ для продукта
class ProductContent(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    icon: Optional[str]
    category_name: Optional[str]
    is_visible: bool
    is_deleted: bool
    category_id: int


class ProductResponse(BaseResponse):
    content: ProductContent


class ProductsListContent(BaseModel):
    products: List[ProductContent]


class ProductsListResponse(BaseResponse):
    content: ProductsListContent


# Ответ для категорий
class CategoryContent(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    is_deleted: bool
    is_visible: bool


class CategoryResponse(BaseResponse):
    content: CategoryContent


class CategoriesListContent(BaseModel):
    categories: List[CategoryContent]


class CategoriesListResponse(BaseResponse):
    content: CategoriesListContent


# Универсальный ответ для сообщений
class MessageContent(BaseModel):
    message: str


class MessageResponse(BaseResponse):
    content: MessageContent


# ======= ВХОДНЫЕ ДАННЫЕ =======

# Входные данные для авторизации/регистрации
class LoginData(BaseModel):
    username: str
    password: str


class RegisterData(BaseModel):
    username: str
    password: str
    confirm_password: str


# Входные данные для продукта
class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int
    description: Optional[str] = None
    icon: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# Входные данные для категорий
class CategoryBase(BaseModel):
    name: str
    description: str
    icon: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# Входные данные для обновления профиля
class UpdateClientDetailsRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    icon: Optional[str] = None
