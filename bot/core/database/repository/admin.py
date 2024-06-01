from ..orm.main_repository import SqlAlchemyRepository
from ..models.admin import AdminOrm

class AdminRepository(SqlAlchemyRepository):
    model = AdminOrm