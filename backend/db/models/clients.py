from sqlalchemy import Column, String, Boolean

from backend.db.base import BaseModel, CleanModel
from .roles import RoleModel


class Clients(BaseModel, CleanModel):
    """Таблица юзеров"""
    __tablename__ = 'clients'

    first_name = Column(String, nullable=True, unique=False)
    last_name = Column(String, nullable=True, unique=False)
    phone_number = Column(String, nullable=True, unique=False)
    email = Column(String, nullable=True, unique=False)
    username = Column(String, nullable=False, unique=True) # важно
    password = Column(String, nullable=False) # важно
    icon = Column(String, nullable=True, unique=False)
    is_banned = Column(Boolean, nullable=False, unique=False, default=False)
    is_deleted = Column(Boolean, nullable=False, unique=False, default=False)
    role = Column(String, nullable=False, default=RoleModel.user)  # user, moderator, admin

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<Users:{self.id}>"

    def __repr__(self):
        return self.__str__()
