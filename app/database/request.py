from app.database.models import User, Queue, Group, Follow, async_session
from sqlalchemy import select


# async def get_queues():
#     async with async_session() as session:
#         result = await session.execute(select(Queue))
#         queues = result.scalars().all()
#         queue_info = '\n'.join([f"Queue ID: {queue.id}, Queue Name: {queue.queue_name}" for queue in queues])
#         return queue_info

async def get_queues():
    async with async_session() as session:
        result = await session.scalars(select(Queue))
        return result


async def add_queue(queue_name):
    async with async_session() as session:
        new_queue = Queue(queue_name=queue_name)
        session.add(new_queue)
        await session.commit()


async def add_user(user_id, user_name):
    async with async_session() as session:
        async with session.begin():
            exists = await session.execute(
                select(User.tg_id).filter(User.tg_id == user_id)
            )
            user = exists.scalar()

            if user is None:
                new_user = User(tg_id=user_id, nickname=user_name)
                session.add(new_user)
                return False
            else:
                return True


async def get_user_nickname(user_id):
    async with async_session() as session:
        result = await session.execute(select(User.nickname).filter(User.tg_id == user_id))
        user = result.scalar()
        return user


async def get_positions(queue_id):
    async with async_session() as session:
        result = await session.execute(select(Follow).filter(Follow.following_queue_id == queue_id))
        positions = result.scalars().all()
        return positions


async def get_queue(queue_id):
    async with async_session() as session:
        result = await session.execute(select(Queue.queue_name).filter(Queue.id == queue_id))
        queue = result.scalar()
        return queue

