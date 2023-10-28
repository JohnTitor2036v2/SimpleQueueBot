from app.database.models import User, Queue, Group, async_session
from sqlalchemy import select


async def get_queues():
    async with async_session() as session:
        result = await session.execute(select(Queue))
        return result


async def add_queue(queue_name):
    async with async_session() as session:
        new_queue = Queue(queue_name=queue_name)
        session.add(new_queue)
        await session.commit()


async def add_user(user_id):
    # user =
    async with async_session() as session:
        new_user = User(user_id=user_id)
        session.add(new_user)
        await session.commit()
