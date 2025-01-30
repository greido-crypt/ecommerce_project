from typing import Optional, List, Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int
    errors: List[str] = []
    content: Optional[Any] = None


class Token:
    class _TokenContent(BaseModel):
        access_token: str
        refresh_token: str
        token_type: str

    class TokenResponse(BaseResponse):
        content: 'Token._TokenContent'


class Profile:
    class ProfileContent(BaseModel):
        id: int
        username: str
        email: Optional[str]
        first_name: Optional[str]
        last_name: Optional[str]
        phone_number: Optional[str]
        icon: Optional[str]
        role: str

    class ProfileResponse(BaseResponse):
        content: 'Profile.ProfileContent'


class Profiles:
    class ProfilesResponse(BaseResponse):
        content: List['Profile.ProfileContent']


class Product:
    class ProductContent(BaseModel):
        id: int
        name: str
        description: Optional[str]
        price: float
        icon: Optional[str]
        is_deleted: bool
        is_visible: bool
        category_name: Optional[str]

    class ProductResponse(BaseResponse):
        content: 'Product.ProductContent'


class Products:
    class _ProductsContent(BaseModel):
        products: List['Product.ProductContent']

    class ProductsResponse(BaseResponse):
        content: 'Products._ProductsContent'


class Category:
    class CategoryContent(BaseModel):
        id: int
        name: str
        description: Optional[str]
        icon: Optional[str]
        is_visible: bool
        is_deleted: bool

    class CategoryResponse(BaseResponse):
        content: 'Category.CategoryContent'


class Categories:
    class _CategoriesContent(BaseModel):
        categories: List[Category.CategoryContent]

    class CategoriesResponse(BaseResponse):
        content: 'Categories._CategoriesContent'


class MessageContent(BaseModel):
    message: str


class MessageResponse(BaseResponse):
    content: MessageContent


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
    is_visible: Optional[bool] = True


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    is_visible: Optional[bool] = None
