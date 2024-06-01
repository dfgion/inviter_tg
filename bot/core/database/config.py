from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from ..config import Config 

engine = create_async_engine(
        url=Config.DATABASE_DSN,
        echo=False,
    )

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)