from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import DatabaseEngine
from backend.db.models import Clients


class ClientsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def addClient(self, password: str, username: str) -> bool:
        """Добавление нового клиента"""
        async with self.session_maker() as session:
            async with session.begin():
                user = Clients(username=username, password=password)
                try:
                    session.add(user)
                    await session.commit()
                except Exception:
                    await session.rollback()
                    return False
                return True

    async def getClientByUsername(self, username: str) -> Optional[Clients]:
        """Получение клиента по имени пользователя"""
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(select(Clients).filter_by(username=username))
                return result.scalars().first()

    async def updateClientPassword(self, username: str, new_password: str) -> bool:
        """Обновление пароля клиента"""
        async with self.session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Clients)
                    .where(Clients.username == username)
                    .values(password=new_password)
                )
                await session.execute(stmt)
                await session.commit()
                return True

    async def getAllClients(self) -> Sequence[Clients]:
        """Получение всех клиентов"""
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(select(Clients))
                return result.scalars().all()

    async def getClientById(self, client_id: int) -> Optional[Clients]:
        """Получение клиента по ID"""
        async with self.session_maker() as session:
            async with session.begin():
                result = await session.execute(select(Clients).filter_by(id=client_id))
                return result.scalars().first()

    async def updateClientDetailsById(
            self,
            client_id: int,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            phone_number: Optional[str] = None,
            email: Optional[str] = None
    ) -> bool:
        """Обновление данных клиента по client_id"""
        async with self.session_maker() as session:
            async with session.begin():
                sql = update(Clients).values(
                    {
                        Clients.first_name: first_name,
                        Clients.last_name: last_name,
                        Clients.phone_number: phone_number,
                        Clients.email: email
                    }
                ).where(Clients.id == client_id)
                await session.execute(sql)
                await session.commit()
                return True

    async def updateClientDetailsByUsername(
            self,
            username: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            icon: Optional[str] = None,
    ) -> bool:
        """Обновление данных клиента по имени пользователя"""
        async with self.session_maker() as session:
            async with session.begin():
                sql = update(Clients).values(
                    {
                        Clients.first_name: first_name,
                        Clients.last_name: last_name,
                        Clients.phone_number: phone_number,
                        Clients.email: email,
                        Clients.icon: icon,
                    }
                ).where(Clients.username == username)
                await session.execute(sql)
                await session.commit()
                return True
