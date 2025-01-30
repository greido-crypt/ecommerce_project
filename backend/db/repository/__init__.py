from .products_repo import ProductsRepository
from .clients_repo import ClientsRepository
from .categories_repo import CategoriesRepository


clients_repository = ClientsRepository()
products_repository = ProductsRepository()
categories_repository = CategoriesRepository()

__all__ = ['clients_repository',
           'products_repository',
           'categories_repository']


