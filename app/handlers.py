from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello there!', reply_markup=kb.main)


@router.message(F.text == 'Show Queue')
async def cmd_show_queue(message: Message):
    await message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue_keyboard_button())


@router.callback_query(F.text.startswith('queue_'))
async def queue_selected(message: Message):
    queue_id = message.data.split('_')[1]
    await message.answer(f'You selected queue {queue_id}')
