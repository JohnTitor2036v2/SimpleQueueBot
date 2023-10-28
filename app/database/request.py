from app.database.models import User, Queue, Group, async_session
from sqlalchemy import select


async def get_queues():
    async with async_session() as session:
        result = await session.execute(select(Queue))
        queues = result.scalars().all()  # Fetch all rows from the result
        queue_info = '\n'.join([f"Queue ID: {queue.id}, Queue Name: {queue.queue_name}" for queue in queues])
        return queue_info


async def add_queue(queue_name):
    async with async_session() as session:
        new_queue = Queue(queue_name=queue_name)
        session.add(new_queue)
        await session.commit()


async def add_user(user_id, user_name):
    async with async_session() as session:
        async with session.begin():
            # Perform a query using execute method
            exists = await session.execute(
                select(User.tg_id).filter(User.tg_id == user_id)
            )
            user = exists.scalar()  # Retrieve the result

            if user is None:
                new_user = User(tg_id=user_id, nickname=user_name)
                session.add(new_user)
                return False
            else:
                return True
