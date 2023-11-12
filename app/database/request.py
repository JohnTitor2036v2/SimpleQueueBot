from app.database.models import User, Queue, Group, Follow, async_session
from sqlalchemy import select
import logging


# async def get_queues():
#     async with async_session() as session:
#         result = await session.execute(select(Queue))
#         queues = result.scalars().all()
#         queue_info = '\n'.join([f"Queue ID: {queue.id}, Queue Name: {queue.queue_name}" for queue in queues])
#         return queue_info

async def get_group_queues(chat_id):
    async with async_session() as session:
        async with session.begin():
            queues = await session.execute(
                select(Queue.queue_name).where(Queue.chat_id == chat_id)
            )
            logging.info(f"Received message: {queues}")
            to_string = ""
            count = 1
            for row in queues:
                to_string = to_string + f"{count}. {row.queue_name}\n"
                count += 1
            return to_string


async def add_queue(chat_id, queue_name, size):
    async with async_session() as session:
        async with session.begin():
            logging.info(f"Received message: {chat_id, queue_name, size}")
            exists = await session.execute(
                select(Queue.chat_id, Queue.queue_name).where(Queue.chat_id == chat_id, Queue.queue_name == queue_name)
            )
            user = exists.scalar()
            logging.info(f"Received message: {user}")

            if user is None:
                new_queu = Queue(queue_name=queue_name, chat_id=chat_id, size=size)
                session.add(new_queu)
                return False
            else:
                return True

async def add_user(new_id, user_name):
    async with async_session() as session:
        async with session.begin():
            exists = await session.execute(
                select(User.user_id).filter(User.user_id == new_id)
            )
            user = exists.scalar()

            if user is None:
                new_user = User(user_id=new_id, nickname=user_name)
                session.add(new_user)
                return False
            else:
                return True
            
async def add_chat(chat_id, chat_name):
    async with async_session() as session:
        async with session.begin():
            exists = await session.execute(
                select(Group.chat_id).filter(Group.chat_id == chat_id)
            )
            chat = exists.scalar()

            if chat is None:
                new_chat = Group(chat_id=chat_id, chat_name=chat_name)
                session.add(new_chat)
                return False
            else:
                return True


async def get_user_nickname(user_id):
    async with async_session() as session:
        result = await session.execute(select(User.nickname).filter(User.user_id == user_id))
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

