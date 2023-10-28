from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello there!', reply_markup=await kb.main())


@router.message(F.text == 'Show Queue')
async def queue(message: Message):
    await message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue())


@router.callback_query(F.data.startswith('queue_'))
async def queue_selected(callback: CallbackQuery):
    queue_id = callback.data.split('_')[1]
    await callback.messge.answer(f'You selected queue {queue_id}')
    await callback.answer(f'Selected')
