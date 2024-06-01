import uuid

from sqlalchemy.orm import Mapped, mapped_column


from .base import Model

class MessageOrm(Model):
    __tablename__ = "message"
    
    entry_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    text: Mapped[str] = mapped_column(nullable=False, unique=False)
    
    def serialize(self):
        return self.text