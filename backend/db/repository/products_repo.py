from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import DatabaseEngine
from backend.db.models import Products


class ProductsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def addProduct(self, name: str, price: float, category_id: int, description: Optional[str] = None, icon: Optional[str] = None) -> bool:
        """Добавление нового товара"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                product = Products(name=name, description=description, icon=icon, price=price, category_id=category_id)
                try:
                    session.add(product)
                except Exception:
                    return False
                return True

    async def getProductById(self, product_id: int) -> Optional[Products]:
        """Получение товара по ID"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Products).filter_by(id=product_id))
                return result.scalars().first()

    async def getProductsByCategoryId(self, category_id: int) -> Sequence[Products]:
        """Получение товаров по ID категории"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Products).filter_by(category_id=category_id))
                return result.scalars().all()

    async def getAllProducts(self) -> Sequence[Products]:
        """Получение всех товаров"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Products))
                return result.scalars().all()

    async def updateProduct(self,
                            product_id: int,
                            name: Optional[str] = None,
                            description: Optional[str] = None,
                            icon: Optional[str] = None,
                            price: Optional[float] = None,
                            category_id: Optional[int] = None) -> bool:
        """Обновление данных товара по ID"""
        product = await self.getProductById(product_id=product_id)
        if not product:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Products)
                    .where(Products.id == product_id)
                    .values(
                        name=name or product.name,
                        description=description or product.description,
                        icon=icon or product.icon,
                        price=price or product.price,
                        category_id=category_id or product.category_id
                    )
                )
                await session.execute(stmt)
                await session.commit()
                return True

    async def deleteProduct(self, product_id: int) -> bool:
        """Удаление товара (помечаем как удалённый/восстановленный)"""
        product = await self.getProductById(product_id=product_id)
        if not product:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Products)
                    .where(Products.id == product_id)
                    .values(is_deleted=not product.is_deleted)
                )
                await session.execute(stmt)
                await session.commit()
                return True

    async def hideProduct(self, product_id: int) -> bool:
        """Скрытие товара (меняем видимость)"""
        product = await self.getProductById(product_id=product_id)
        if not product:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Products)
                    .where(Products.id == product_id)
                    .values(is_visible=not product.is_visible)
                )
                await session.execute(stmt)
                await session.commit()
                return True
