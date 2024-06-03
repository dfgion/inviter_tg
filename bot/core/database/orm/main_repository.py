import uuid
from sqlalchemy import select, update

from .base import AbstractRepository

from ..config import async_session


class SqlAlchemyRepository(AbstractRepository):
    model = None

    
    @classmethod
    async def get_objects(cls) -> list:
        async with async_session() as session:
            stmt = (
                select(cls.model)
            )
            objects = list((await session.execute(stmt)).scalars().unique().all())
            if not objects:
                return []
    
        return [db_object.serialize() for db_object in objects]
    
    @classmethod    
    async def insert_object(
        cls,
        data: dict
    ):
        async with async_session() as session:
            new_object = cls.model(**data)
            session.add(new_object)
            await session.flush()
            await session.commit()          
    
    @classmethod
    async def update_object(
        cls,
        entry_id: int | uuid.UUID,
        data: dict
    ):
        async with async_session() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.entry_id == entry_id)
                .values(**data)
            )
            await session.execute(stmt)
            await session.commit()   
            
            