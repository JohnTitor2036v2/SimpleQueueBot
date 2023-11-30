from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from instances_for_main import bot

import app.keyboards as kb
import app.database.request as rq

router = Router()
# ALLOWED_ADMIN = []


async def admin_filter(user_id, chat_id):
    admins = await bot.get_chat_administrators(chat_id)
    for admin in admins:
        if user_id == admin.user.id:
            return True
    return False


@router.callback_query(F.data == 'switch_user_position')
async def switch(callback: CallbackQuery):
    await callback.message.answer('Im here')
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if await admin_filter(user_id, chat_id):
        # ALLOWED_ADMIN.clear()
        # ALLOWED_ADMIN.append(user_id)
        await callback.message.answer(
            'Select a queue to change the users position',
            reply_markup=await kb.switch_first_step(chat_id)
        )
    else:
        await callback.message.answer(f'{callback.from_user.first_name} u dnt hace access to this fnctn')


@router.callback_query(F.data.startwith('first_'))
async def switch_first(callback: CallbackQuery):
    await callback.message.answer('Im also here')
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)

    await callback.message.answer(
        'Select a user to change their position',
        reply_markup=await kb.switch_second_step(queue_id)
    )

# @router.callback_query(F.data == '')
