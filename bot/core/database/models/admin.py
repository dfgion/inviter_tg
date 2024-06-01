import uuid

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


from .base import Model

class AdminOrm(Model):
    __tablename__ = "admins"
    
    entry_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger(), nullable=False, unique=True)
    
    def serialize(self):
        return self.telegram_id