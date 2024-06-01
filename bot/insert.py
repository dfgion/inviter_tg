import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import models
from core.database.config import async_session

from core.config import Config


async def insert_admins(session: AsyncSession):
    admin = models.admin.AdminOrm(
        telegram_id=Config.SUPER_ADMIN, 
    )
    session.add(admin)
    await session.flush()
    
async def insert_message(session: AsyncSession):
    message = models.message.MessageOrm(
        entry_id = 1,
        text='Ваша заявка скоро будет одобрена в порядке очереди ✅\n\nЧтобы ускорить, подпишитесь на следующие каналы:', 
    )
    session.add(message)
    await session.flush()


async def main():
    async with async_session() as session:
        await insert_admins(session)
        await insert_message(session)
        await session.commit()
        
asyncio.run(main())