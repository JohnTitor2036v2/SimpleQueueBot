from aiogram import Router, F
from aiogram.types import Message, User
from aiogram.types.chat import Chat
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.database.request as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello there!', reply_markup=kb.main)

@router.message(Command('createqueue'))
async def cmd_create(message: Message):
    rq.new_queue(
    tg_id = User.id,
    nickname = User.username,
    tg_group_id = Chat.id,
    group_name = Chat.username,
    name = 1,
    position = 1
    )
    await message.answer('Queue created.')

@router.message(F.text == 'Show Queue')
async def cmd_show_queue(message: Message):
    await message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue_keyboard_button())


@router.callback_query(F.text.startswith('queue_'))
async def queue_selected(message: Message):
    queue_id = message.data.split('_')[1]
    await message.answer(f'You selected queue {queue_id}')
