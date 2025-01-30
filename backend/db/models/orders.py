from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, Mapped

from backend.db.base import BaseModel, CleanModel
from .clients import Clients
from .products import Products

class Orders(BaseModel, CleanModel):
    """Таблица юзеров"""
    __tablename__ = 'orders'

    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False)
    product: Mapped[Products] = relationship(Products.__name__, backref=Products.__name__ + __tablename__, cascade='all', lazy='subquery')

    client_id = Column(BigInteger, ForeignKey('clients.id'), nullable=False)
    client: Mapped[Clients] = relationship(Clients.__name__, backref=Clients.__name__ + __tablename__, cascade='all', lazy='subquery')

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<Orders:{self.id}>"

    def __repr__(self):
        return self.__str__()
