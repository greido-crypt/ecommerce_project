from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped
from backend.db.base import BaseModel, CleanModel
from .categories import Categories


class Products(BaseModel, CleanModel):
    """Таблица товаров"""
    __tablename__ = 'products'

    name = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=True)
    icon = Column(String, unique=False, nullable=True)
    price = Column(Float, nullable=False)
    is_visible = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category: Mapped[Categories] = relationship(Categories.__name__, backref=__tablename__, lazy="subquery")

    def __str__(self) -> str:
        return f"<Product:{self.id}, Name:{self.name}, Category:{self.category.name}>"

    def __repr__(self):
        return self.__str__()
