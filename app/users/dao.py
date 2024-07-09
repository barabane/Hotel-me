from sqlalchemy import select
from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import nullpool_session_maker


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_by_id_nullpool(cls, id: int):
        async with nullpool_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
