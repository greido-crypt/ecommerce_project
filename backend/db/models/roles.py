from typing import ClassVar

from pydantic import BaseModel


class Role(BaseModel):
    user: ClassVar[str] = 'user'
    admin: ClassVar[str] = 'admin'
    moderator: ClassVar[str] = 'moderator'


RoleModel = Role()