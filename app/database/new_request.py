from app.database.new_models import User, Queue, Group, Follow, async_session
from sqlalchemy import select, asc, delete, func, update, insert
import logging


# INSERT
async def add_group(group_id, group_name, group_type):
    async with async_session() as session:
        async with session.begin():
            group = await session.execute(
                select(Group.group_id)
                .filter_by(group_id=group_id)
            )
            group = group.scalar()

            if group is None:
                session.add(Group(group_id=group_id, group_name=group_name, group_type=group_type))
                return False
            else:
                return True


async def add_user(user_id, nickname):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User.user_id)
                .filter_by(user_id=user_id)
            )
            user = user.scalar()

            if user is None:
                session.add(User(user_id=user_id, nickname=nickname))
                return False
            else:
                return True


async def add_queue(group_id, queue_name, size):
    async with async_session() as session:
        async with session.begin():
            queue = await session.execute(
                select(Queue.group_id, Queue.queue_name)
                .filter_by(group_id=group_id, queue_name=queue_name)
            )
            queue = queue.scalar()

            if user is None:
                session.add(Queue(queue_name=queue_name, group_id=group_id, size=size))
                return False
            else:
                return True


# SELECT
async def get_user_nickname(user_id):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User.nickname)
                .filter_by(user_id=user_id)
            )
            return user.scalar()


async def get_queues(group_id):
    async with async_session() as session:
        async with session.begin():
            queues = await session.execute(
                select(Queue)
                .filter_by(group_id=group_id)
                .order_by(asc(Queue.queue_id))
            )
            return queues.scalars().all()


async def get_positions(queue_id):
    async with async_session() as session:
        async with session.begin():
            positions = await session.execute(
                select(Follow)
                .filter_by(queue_id=queue_id)
                .order_by(asc(Follow.user_position))
            )
            return positions.scalars().all()


async def get_queue_max_size(queue_id):
    async with async_session() as session:
        async with session.begin():
            max_position = await session.execute(
                select(Queue.size)
                .filter_by(queue_id=queue_id)
            )
            return max_position.scalar()


async def get_queue(queue_id):
    async with async_session() as session:
        async with session.begin():
            queue = await session.execute(
                select(Queue.queue_name)
                .filter_by(queue_id=queue_id)
            )
            return queue.scalar()


async def get_queue_id(group_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            queue_id = await session.execute(
                select(Queue.queue_id)
                .filter_by(group_id=group_id, queue_name=queue_name)
            )
            return queue_id.scalar()


async def get_user_position(user_id, queue_id):
    async with async_session() as session:
        async with session.begin():
            position = await session.execute(
                select(Follow.user_position)
                .filter_by(user_id=user_id, queue_id=queue_id)
            )
            return position.scalar()


async def get_user_id_by_position(queue_id, user_position):
    async with async_session() as session:
        async with session.begin():
            user_id = await session.execute(
                select(Follow.user_id)
                .filter_by(queue_id=queue_id, user_position=user_position)
            )
            return user_id.scalar()


# UPDATE
async def join_queue(user_id, group_id, queue_name):
    async with async_session() as session:
        async with session.begin():
            queue_id = await session.execute(
                select(Queue.queue_id)
                .filter_by(group_id=group_id, queue_name=queue_name)
            )  # .scalar()
            queue_id = queue_id.scalar()

            follow_exists = await session.execute(
                select(Follow)
                .filter_by(user_id=user_id, queue_id=queue_id)
            )  # .scalar()
            follow_exists = follow_exists.scalar()

            if follow_exists is None:
                positions_taken = await session.execute(
                    select(Follow.user_position)
                    .filter_by(queue_id=queue_id)
                    .order_by(asc(Follow.user_position))
                )  # .scalars().all()
                positions_taken = positions_taken.scalars().all()

                if positions_taken:
                    position = max(positions_taken) + 1
                else:
                    position = 1

                session.add(Follow(user_id=user_id, queue_id=queue_id, user_position=position))
                return False
            else:
                return True


async def switch_positions(queue_id, new_position, old_position):
    async with async_session() as session:
        async with session.begin():
            follow1 = await session.execute(
                select(Follow)
                .filter_by(queue_id=queue_id, user_position=old_position)
            )
            follow1 = follow1.scalar()

            if not follow1:
                return False

            follow2 = await session.execute(
                select(Follow)
                .filter_by(queue_id=queue_id, user_position=new_position)
            )
            follow2 = follow2.scalar()

            if not follow2:
                follow1.user_position = new_position
            else:
                follow1.user_position = new_position
                follow2.user_position = old_position

            return True


# DELETE
async def delete_queue(queue_id):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                delete(Queue)
                .filter_by(queue_id=queue_id)
            )
            return True


async def leave_queue(user_id, queue_id):
    async with async_session() as session:
        async with session.begin():
            follow_exists = await session.execute(
                select(Follow)
                .filter_by(user_id=user_id, queue_id=queue_id)
            )
            follow_exists = follow_exists.scalar()

            if follow_exists is not None:
                await session.execute(
                    delete(Follow)
                    .filter_by(user_id=user_id, queue_id=queue_id)
                )
                return False
            else:
                return True
