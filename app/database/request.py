from app.database.models import User, Queue, Group, async_session
from sqlalchemy import select


async def get_queues():
    async with async_session() as session:
        result = await session.execute(select(Queue))
        return result
