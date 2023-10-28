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


async def add_user(user_id, user_name):
    async with async_session() as session:
        exists = await session.query(User).filter_by(id=user_id).first()
        if exists:
            return True
        else:
            new_user = User(id=user_id, nickname=user_name)
            session.add(new_user)
            session.commit()
            return False


async def get_user_nickname(user_id):
    async with async_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return {'nickname': user.nickname}
        else:
            return {'nickname': None}
