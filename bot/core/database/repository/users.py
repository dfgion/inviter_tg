from ..orm.main_repository import SqlAlchemyRepository
from ..models.users import UserOrm

class UserRepository(SqlAlchemyRepository):
    model = UserOrm