from ..orm.main_repository import SqlAlchemyRepository
from ..models.message import MessageOrm

class MessageRepository(SqlAlchemyRepository):
    model = MessageOrm