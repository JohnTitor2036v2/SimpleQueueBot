from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.request as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if not rq.add_user(User.id, User.first_name):
        await message.answer(f'Welcome, {User.first_name}', reply_markup=await kb.main())
    else:
        nickname = rq.get_user_nickname(User.id)
        await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.main())


@router.message(Command('showqueue'))
async def cmd_show_all(message: Message):
    queues = await rq.get_queues()
    await message.answer(queues)


@router.message(F.text == 'Show Queue')
async def queue(message: Message):
    await message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue())


@router.callback_query(F.data.startswith('queue_'))
async def queue_selected(callback: CallbackQuery):
    queue_id = callback.data.split('_')[1]
    await callback.messge.answer(f'You selected queue {queue_id}')
    await callback.answer(f'Selected')
