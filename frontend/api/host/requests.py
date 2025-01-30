from frontend.api.default import BaseRequest
from .models import Token, MessageResponse, Profile, Category, Categories, Products, Product, Profiles


class HostApi(BaseRequest):
    def __init__(self,
                 access_token: str = None,
                 refresh_token: str = None,
                 base_url: str = 'http://127.0.0.1:8000/api/v1'
                 ):
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        headers = {"Authorization": f"Bearer {self.__access_token}"} if self.__access_token else {}

        super().__init__(base_url=base_url, headers=headers, timeout=10)

    # User Authentication
    async def signUp(self, username: str, password: str, confirm_password: str):
        json_data = {"username": username, "password": password, "confirm_password": confirm_password}
        response = await self._post(endpoint='signup', json=json_data)
        return Token.TokenResponse.model_validate_json(response.text)

    async def login(self, username: str, password: str):
        json_data = {"username": username, "password": password}
        response = await self._post(endpoint='login', json=json_data)
        return Token.TokenResponse.model_validate_json(response.text)

    # User Profile
    async def getProfile(self):
        response = await self._get(endpoint='get_profile')
        return Profile.ProfileResponse.model_validate_json(response.text)

    async def getAllClients(self):
        response = await self._get(endpoint='get_all_clients')
        return Profiles.ProfilesResponse.model_validate_json(response.text)

    # Category Management
    async def getCategory(self, category_id: int):
        response = await self._get(endpoint=f'get_category/{category_id}')
        return Category.CategoryResponse.model_validate_json(response.text)

    async def getAllCategories(self):
        response = await self._get(endpoint='get_all_categories')
        return Categories.CategoriesResponse.model_validate_json(response.text)

    async def getProductsByCategory(self, category_id: int):
        response = await self._get(endpoint=f'get_products/{category_id}')
        return Products.ProductsResponse.model_validate_json(response.text)

    async def getAllProducts(self):
        response = await self._get(endpoint='get_all_products')
        return Products.ProductsResponse.model_validate_json(response.text)

    async def getProduct(self, product_id: int):
        response = await self._get(endpoint=f'get_product/{product_id}')
        return Product.ProductResponse.model_validate_json(response.text)

    async def updateClientDetails(self,
                                  first_name: str = None,
                                  last_name: str = None,
                                  phone_number: str = None,
                                  email: str = None,
                                  icon: str = None):
        json_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email,
            "icon": icon,
        }
        response = await self._post(endpoint='update_client_details', json=json_data)
        return MessageResponse.model_validate_json(response.text)

    # === CATEGORY ===

    async def deleteCategory(self, category_id: int):
        response = await self._delete(endpoint=f'delete_category/{category_id}')
        return MessageResponse.model_validate_json(response.text)

    async def hideCategory(self, category_id: int) -> MessageResponse:
        response = await self._put(endpoint=f'hide_category/{category_id}')
        return MessageResponse.model_validate_json(response.text)

    async def updateCategory(self,
                             category_id: int,
                             name: str = None,
                             description: str = None,
                             icon: str = None):
        json_data = {
            "name": name,
            "description": description,
            "icon": icon,
        }
        response = await self._post(endpoint=f'update_category/{category_id}', json=json_data)
        return MessageResponse.model_validate_json(response.text)

    async def addCategory(self,
                          name: str = None,
                          description: str = None,
                          icon: str = None):
        json_data = {
            "name": name,
            "description": description,
            "icon": icon,
        }
        response = await self._post(endpoint=f'add_category', json=json_data)
        return MessageResponse.model_validate_json(response.text)

    # === CATEGORY ===

    # === Product ===

    async def addProduct(self,
                         category_id: int,
                         price: float,
                         name: str = None,
                         description: str = None,
                         icon: str = None):
        json_data = {
            "name": name,
            "price": price,
            "category_id": category_id,
            "description": description,
            "icon": icon
        }
        response = await self._post(endpoint=f'add_product', json=json_data)
        return MessageResponse.model_validate_json(response.text)

    async def deleteProduct(self, product_id: int):
        response = await self._delete(endpoint=f'delete_product/{product_id}')
        return MessageResponse.model_validate_json(response.text)

    async def updateProduct(self,
                            category_id: int = None,
                            product_id: int = None,
                            price: float = None,
                            name: str = None,
                            description: str = None,
                            icon: str = None):
        json_data = {
            "name": name,
            "price": price,
            "category_id": category_id,
            "description": description,
            "icon": icon
        }
        response = await self._post(endpoint=f'update_product/{product_id}', json=json_data)
        return MessageResponse.model_validate_json(response.text)

    async def hideProduct(self, product_id: int):
        response = await self._put(endpoint=f'hide_product/{product_id}')
        return MessageResponse.model_validate_json(response.text)

    # === Product ===
