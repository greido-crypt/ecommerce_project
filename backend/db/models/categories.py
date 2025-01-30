from typing import Dict, Any

from sqlalchemy import Column, String, Boolean

from backend.db.base import BaseModel, CleanModel


class Categories(BaseModel, CleanModel):
    """Таблица юзеров"""
    __tablename__ = 'categories'
    name = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=False)
    icon = Column(String, unique=False, nullable=False)
    is_visible = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> dict[str, Any]:
        return self.__dict__

    def __repr__(self):
        return self.__str__()
