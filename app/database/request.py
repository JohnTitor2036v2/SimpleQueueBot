from app.database.models import User, Queue, Group, Follow, async_session
from sqlalchemy import select, asc, delete, func, update
import logging


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
                logging.info(f"FINAL SQL: INSERT INTO queues (queue_name, chat_id, size) VALUES ({queue_name}, {chat_id}, {size})")
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
                logging.info(f"FINAL SQL: INSERT INTO users (user_id, nickname) VALUES ({new_id}, {user_name})")
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
                logging.info(f"FINAL SQL: INSERT INTO groups (chat_id, chat_name) VALUES ({chat_id}, {chat_name})")
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
        result = await session.execute(select(Follow).filter(Follow.following_queue_id == int(queue_id)))
        positions = result.scalars().all()
        return positions


async def get_queue(queue_id):
    async with async_session() as session:
        result = await session.execute(select(Queue.queue_name).filter(Queue.id == queue_id))
        queue = result.scalar()
        return queue


async def get_queues(chat_id):
    async with async_session() as session:
        result = await session.execute(select(Queue).filter(Queue.chat_id == chat_id))
        queues = result.scalars().all()
        return queues


async def get_queue_max_size(queue_id):
    async with async_session() as session:
        result = await session.execute(select(Queue.size).filter(Queue.id == queue_id))
        max_position = result.scalar()
        return max_position


async def join_queue(user_id, chat_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Queue.id).where(Queue.chat_id == chat_id, Queue.queue_name == queue_name)
            )
            queue_id = result.scalar()

            follow_exists_result = await session.execute(
                select(Follow).where(Follow.following_user_id == user_id,
                                     Follow.following_queue_id == queue_id)
            )
            follow_exists = follow_exists_result.scalar()

            if follow_exists is None:
                position_result = await session.execute(
                    select(Follow.position).where(Follow.following_queue_id == queue_id).order_by(asc(Follow.position))
                )
                positions_taken = [row for row in position_result.scalars()]

                if positions_taken:
                    available_positions = set(range(1, max(positions_taken) + 2)) - set(positions_taken)
                    new_position = min(available_positions)
                else:
                    new_position = 1

                follow_row = Follow(following_user_id=user_id, following_queue_id=queue_id, position=new_position)
                session.add(follow_row)
                logging.info(f"FINAL SQL: INSERT INTO follows (following_user_id, following_queue_id, position) VALUES ({user_id}, {queue_id}, {new_position})")
                return False
            else:
                return True


async def leave_queue(user_id, chat_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Queue.id).where(Queue.chat_id == chat_id, func.lower(Queue.queue_name) == func.lower(queue_name))
            )
            queue_id = result.scalar()

            follow_exists_result = await session.execute(
                select(Follow).where(Follow.following_user_id == user_id, Follow.following_queue_id == queue_id)
            )
            follow_exists = follow_exists_result.scalar()

            if follow_exists is not None:
                await session.execute(
                    delete(Follow).where(Follow.following_user_id == user_id, Follow.following_queue_id == queue_id)
                )
                logging.info(f"FINAL SQL: DELETE FROM follows WHERE (following_user_id, following_queue_id) VALUES ({user_id}, {queue_id})")
                return False
            else:
                return True


async def delete_queue(chat_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Queue.id).where(Queue.chat_id == chat_id, func.lower(Queue.queue_name) == func.lower(queue_name))
            )
            queue_id = result.scalar()

            if queue_id is not None:
                await session.execute(
                    delete(Follow).where(Follow.following_queue_id == queue_id)
                )
                logging.info(f"FINAL SQL: DELETE FROM follows WHERE (following_queue_id) VALUES ({queue_id})")

                await session.execute(
                    delete(Queue).where(Queue.id == queue_id)
                )
                logging.info(f"FINAL SQL: DELETE FROM queues WHERE (id) VALUES ({queue_id})")
                return False
            else:
                return True


async def switch_positions(queue_id, position2, position1):
    async with async_session() as session:
        async with session.begin():
            follow1_result = await session.execute(
                select(Follow).where(Follow.following_queue_id == queue_id, Follow.position == position1)
            )
            follow1 = follow1_result.scalar()

            if not follow1:
                return False
            follow2_result = await session.execute(
                select(Follow).where(Follow.following_queue_id == queue_id, Follow.position == position2)
            )
            follow2 = follow2_result.scalar()
            if follow2 is None:
                follow1.position = position2
            else:
                follow1.position, follow2.position = position2, position1

            return True


async def get_user_id_by_position(queue_id, position):
    async with async_session() as session:
        result = await session.execute(
            select(Follow.following_user_id)
            .where(Follow.following_queue_id == queue_id, Follow.position == position)
        )
        user_id = result.scalar()
        return user_id


async def leave_queue_by_admin(user_id, chat_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Queue.id).where(Queue.chat_id == chat_id, func.lower(Queue.queue_name) == func.lower(queue_name))
            )
            queue_id = result.scalar()

            follow_exists_result = await session.execute(
                select(Follow).where(Follow.following_user_id == user_id, Follow.following_queue_id == queue_id)
            )
            follow_exists = follow_exists_result.scalar()

            if follow_exists is not None:
                await session.execute(
                    delete(Follow).where(Follow.following_user_id == user_id, Follow.following_queue_id == queue_id)
                )
                return False
            else:
                return True


async def get_user_id_by_position_and_queue(queue_id, position):
    async with async_session() as session:
        result = await session.execute(
            select(Follow.following_user_id)
            .where(Follow.following_queue_id == queue_id, Follow.position == position)
        )
        user_id = result.scalar()
        return user_id
