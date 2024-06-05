from ..orm.main_repository import SqlAlchemyAdminRepository
from ..models.admin import AdminOrm

class AdminRepository(SqlAlchemyAdminRepository):
    model = AdminOrm