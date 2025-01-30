from fastapi import APIRouter, HTTPException, Depends

from backend.db.repository import clients_repository, categories_repository, products_repository
from backend.fast_api.models import ProductCreate, ProductUpdate, CategoryUpdate, CategoryCreate
from backend.fast_api.models import (
    RegisterData,
    LoginData,
    TokenResponse,
    ProfileResponse,
    ProductResponse,
    ProductsListResponse,
    CategoriesListResponse,
    CategoryResponse,
    UpdateClientDetailsRequest,
    MessageResponse,
    TokenContent,
    ProductsListContent,
    CategoriesListContent,
    MessageContent, ProductContent, ProfileListResponse, ProfileContent
)
from backend.fast_api.utils import bcrypt_util as bcrypt

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def register(user: RegisterData):
    if user.confirm_password != user.password:
        raise HTTPException(status_code=400, detail="Password mismatch")

    hashed_password = bcrypt.hash_password(user.password)
    client_status = await clients_repository.addClient(password=hashed_password, username=user.username)
    if not client_status:
        raise HTTPException(status_code=400, detail="Error in registration")

    user_data = {"sub": user.username}
    access_token = bcrypt.create_access_token(data=user_data)
    refresh_token = bcrypt.create_refresh_token(data=user_data)

    return TokenResponse(
        status_code=201,
        errors=[],
        content=TokenContent(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(user: LoginData):
    user_data = await clients_repository.getClientByUsername(username=user.username)
    if user_data and bcrypt.verify_password(user.password, user_data.password):
        user_data = {"sub": user_data.username}
        access_token = bcrypt.create_access_token(data=user_data)
        refresh_token = bcrypt.create_refresh_token(data=user_data)

        return TokenResponse(
            status_code=200,
            errors=[],
            content=TokenContent(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
        )

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/get_profile", response_model=ProfileResponse)
async def get_profile(current_user: str = Depends(bcrypt.get_current_user)):
    user = await clients_repository.getClientByUsername(username=current_user)
    if user:
        return ProfileResponse(
            status_code=200,
            errors=[],
            content=user.__dict__
        )
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/get_category/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, current_user: str = Depends(bcrypt.get_current_user)):
    category = await categories_repository.getCategoryById(category_id)
    if category:
        return CategoryResponse(
            status_code=200,
            errors=[],
            content=category.__dict__
        )
    raise HTTPException(status_code=404, detail="Category not found")


@router.get("/get_all_categories", response_model=CategoriesListResponse)
async def get_all_categories(current_user: str = Depends(bcrypt.get_current_user)):
    categories = await categories_repository.getAllCategories()
    return CategoriesListResponse(
        status_code=200,
        errors=[],
        content=CategoriesListContent(
            categories=[category.__dict__ for category in categories]
        )
    )


@router.get("/get_products/{category_id}", response_model=ProductsListResponse)
async def get_products(category_id: int, current_user: str = Depends(bcrypt.get_current_user)):
    products = await products_repository.getProductsByCategoryId(category_id=category_id)

    # Создаём новый список продуктов без параметра 'category'
    products = [
        ProductContent(id=product.id,
                       name=product.name,
                       description=product.description,
                       price=product.price,
                       icon=product.icon,
                       is_visible=product.is_visible,
                       is_deleted=product.is_deleted,
                       category_id=product.category_id,
                       category_name=product.category.name
                       )
        for product in products
    ]

    return ProductsListResponse(
        status_code=200,
        errors=[],
        content=ProductsListContent(
            products=products
        )
    )


@router.get("/get_all_products", response_model=ProductsListResponse)
async def get_products(current_user: str = Depends(bcrypt.get_current_user)):
    products = await products_repository.getAllProducts()

    products = [
        ProductContent(id=product.id,
                       name=product.name,
                       description=product.description,
                       price=product.price,
                       icon=product.icon,
                       is_visible=product.is_visible,
                       is_deleted=product.is_deleted,
                       category_id=product.category_id,
                       category_name=product.category.name
                       )
        for product in products
    ]

    return ProductsListResponse(
        status_code=200,
        errors=[],
        content=ProductsListContent(
            products=products
        )
    )


@router.get("/get_product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, current_user: str = Depends(bcrypt.get_current_user)):
    product = await products_repository.getProductById(product_id)
    if product:
        return ProductResponse(
            status_code=200,
            errors=[],
            content=ProductContent(id=product.id,
                                   name=product.name,
                                   description=product.description,
                                   price=product.price,
                                   icon=product.icon,
                                   is_visible=product.is_visible,
                                   is_deleted=product.is_deleted,
                                   category_id=product.category_id,
                                   category_name=product.category.name
                                   )
        )
    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/update_client_details", response_model=MessageResponse, status_code=200)
async def update_client_details(
        update_data: UpdateClientDetailsRequest,
        current_user: str = Depends(bcrypt.get_current_user)
):
    updated = await clients_repository.updateClientDetailsByUsername(
        username=current_user,
        first_name=update_data.first_name,
        last_name=update_data.last_name,
        phone_number=update_data.phone_number,
        email=update_data.email,
        icon=update_data.icon
    )
    if updated:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Client details updated successfully")
        )
    raise HTTPException(status_code=400, detail="Failed to update client details")


@router.get("/get_all_clients", response_model=ProfileListResponse)
async def get_all_clients(current_user: str = Depends(bcrypt.get_current_user)):
    clients = await clients_repository.getAllClients()

    filtered_clients = [
        ProfileContent(
            id=client.id,
            username=client.username,
            email=client.email,
            first_name=client.first_name,
            last_name=client.last_name,
            phone_number=client.phone_number,
            icon=client.icon,
            is_banned=client.is_banned,
            is_deleted=client.is_deleted,
            role=client.role
        )
        for client in clients
    ]

    return ProfileListResponse(
        status_code=200,
        errors=[],
        content=filtered_clients
    )


async def is_admin(current_user: str = Depends(bcrypt.get_current_user)):
    user = await clients_repository.getClientByUsername(username=current_user)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied. Admin role required.")
    return current_user


@router.post("/add_product", response_model=MessageResponse, status_code=201)
async def add_product(
        product: ProductCreate,
        current_user: str = Depends(is_admin)
):
    success = await products_repository.addProduct(
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        description=product.description,
        icon=product.icon
    )
    if success:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Product successfully added.")
        )

    raise HTTPException(status_code=400, detail="Failed to add product.")


@router.post("/update_product/{product_id}", response_model=MessageResponse)
async def update_product(
        product_id: int,
        product: ProductUpdate,
        current_user: str = Depends(is_admin)
):
    success = await products_repository.updateProduct(
        product_id=product_id,
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        description=product.description,
        icon=product.icon
    )
    if success:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Product successfully updated")
        )

    raise HTTPException(status_code=400, detail="Failed to update product.")


@router.delete("/delete_product/{product_id}", response_model=MessageResponse)
async def delete_product(
        product_id: int,
        current_user: str = Depends(is_admin)
):
    success = await products_repository.deleteProduct(product_id)
    if success:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Product successfully deleted.")
        )

    raise HTTPException(status_code=400, detail="Failed to delete product.")


@router.put("/hide_product/{product_id}", response_model=MessageResponse)
async def hide_product(
        product_id: int,
        current_user: str = Depends(is_admin)
):
    success = await products_repository.hideProduct(product_id)
    if success:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Product successfully hided.")
        )

    raise HTTPException(status_code=400, detail="Failed to hide product.")


@router.post("/add_category", response_model=MessageResponse, status_code=201)
async def add_category(category: CategoryCreate, current_user: str = Depends(is_admin)):
    category_added = await categories_repository.addCategory(
        name=category.name,
        description=category.description,
        icon=category.icon
    )
    if category_added:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Category added successfully")
        )

    raise HTTPException(status_code=400, detail="Failed to add category")


@router.post("/update_category/{category_id}", response_model=MessageResponse)
async def update_category(category_id: int, category: CategoryUpdate, current_user: str = Depends(is_admin)):
    updated = await categories_repository.updateCategory(
        category_id=category_id,
        name=category.name,
        description=category.description,
        icon=category.icon,
    )
    if updated:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Category updated successfully")
        )

    raise HTTPException(status_code=400, detail="Failed to update category")


@router.delete("/delete_category/{category_id}", response_model=MessageResponse)
async def delete_category(category_id: int, current_user: str = Depends(is_admin)):
    deleted = await categories_repository.deleteCategory(category_id=category_id)
    if deleted:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Category deleted successfully")
        )

    raise HTTPException(status_code=400, detail="Failed to delete category")


@router.put("/hide_category/{category_id}", response_model=MessageResponse)
async def delete_category(category_id: int, current_user: str = Depends(is_admin)):
    deleted = await categories_repository.hideCategory(category_id=category_id)
    if deleted:
        return MessageResponse(
            status_code=200,
            errors=[],
            content=MessageContent(message="Category deleted successfully")
        )

    raise HTTPException(status_code=400, detail="Failed to delete category")
