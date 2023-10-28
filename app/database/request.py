from app.database.models import User, Queue, Group, async_session, engine
from sqlalchemy import select

async def new_queue(tg_id, nickname, tg_group_id, group_name, queue_name, position):
    user_stm = User.insert().values(tg_id=tg_id, nickname=nickname)
    engine.execute(user_stm)

    user_id = engine.execute(f'SELECT id FROM users WHERE tg_id = {tg_id}')

    group_stm = Group.insert().values(tg_id=tg_group_id, name=group_name)
    engine.execute(group_stm)

    group_id = engine.execute(f'SELECT id FROM groups WHERE tg_id = {tg_group_id}') 

    queue_stm = Queue.insert().values(queue_name=queue_name, 
                                group_id=group_id,  
                                user_id=user_id,
                                position=position) 
    engine.execute(queue_stm) 

async def get_queues():
    async with async_session() as session:
        result = await session.execute(select(Queue))
        return result
