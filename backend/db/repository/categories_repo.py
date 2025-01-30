from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import DatabaseEngine
from backend.db.models import Categories


class CategoriesRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def addCategory(self, name: str, description: str, icon: str) -> bool:
        """Добавление новой категории"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                category = Categories(name=name, description=description, icon=icon)
                try:
                    session.add(category)
                except Exception:
                    return False
                return True

    async def getCategoryById(self, category_id: int) -> Optional[Categories]:
        """Получение категории по ID"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Categories).filter_by(id=category_id))
                return result.scalars().first()

    async def getCategoryByName(self, name: str) -> Optional[Categories]:
        """Получение категории по имени"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Categories).filter_by(name=name))
                return result.scalars().first()

    async def getAllCategories(self) -> Sequence[Categories]:
        """Получение всех категорий"""
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(Categories))
                return result.scalars().all()

    async def updateCategory(self,
                             category_id: int,
                             name: Optional[str] = None,
                             description: Optional[str] = None,
                             icon: Optional[str] = None) -> bool:
        """Обновление данных категории по ID"""
        category = await self.getCategoryById(category_id=category_id)
        if not category:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Categories)
                    .where(Categories.id == category_id)
                    .values(
                        name=name or category.name,
                        description=description or category.description,
                        icon=icon or category.icon,
                    )
                )
                await session.execute(stmt)
                await session.commit()
                return True

    async def deleteCategory(self, category_id: int) -> bool:
        """Удаление категории (помечаем как удалённую или восстанавливаем)"""
        category = await self.getCategoryById(category_id=category_id)
        if not category:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Categories)
                    .where(Categories.id == category_id)
                    .values(is_deleted=not category.is_deleted)
                )
                await session.execute(stmt)
                await session.commit()
                return True

    async def hideCategory(self, category_id: int) -> bool:
        """Скрытие или отображение категории (меняем видимость)"""
        category = await self.getCategoryById(category_id=category_id)
        if not category:
            return False

        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Categories)
                    .where(Categories.id == category_id)
                    .values(is_visible=not category.is_visible)
                )
                await session.execute(stmt)
                await session.commit()
                return True
