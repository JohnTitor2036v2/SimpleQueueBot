from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from instances_for_main import bot

import app.keyboards as kb
import app.database.new_request as rq

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
    user_id = callback.from_user.id
    group_id = callback.message.chat.id
    if await admin_filter(user_id, group_id):
        await callback.message.answer(
            'Select a queue to change the users position',
            reply_markup=await kb.switch_first_step(group_id)
        )
    else:
        await callback.message.answer(f'{callback.from_user.first_name}, u dont have access to this fnctn')


@router.callback_query(F.data.startswith('first_'))
async def switch_first(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if await admin_filter(user_id, chat_id):
        queue_id_str = callback.data.split('_')[1]
        queue_id = int(queue_id_str)

        await callback.message.answer(
            'Select a user to change their position',
            reply_markup=await kb.switch_second_step(queue_id)
        )
    else:
        await callback.message.answer(f'{callback.from_user.first_name}, u dnt hace access to this fnctn')


@router.callback_query(F.data.startswith('second_'))
async def switch_first(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if await admin_filter(user_id, chat_id):
        position_in_str = callback.data.split('_')[1]
        position = int(position_in_str)
        queue_id_in_str = callback.data.split('_')[2]
        queue_id = int(queue_id_in_str)
        chat_id = callback.message.chat.id

        await callback.message.answer(
            'Select which position you want to change this users position in the queue to',
            reply_markup=await kb.switch_third_step(position, queue_id)
        )
    else:
        await callback.message.answer(f'{callback.from_user.first_name}, u dnt hace access to this fnctn')


@router.callback_query(F.data.startswith('switch_'))
async def switch(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if await admin_filter(user_id, chat_id):
        queue_id_in_str = callback.data.split('_')[1]
        queue_id = int(queue_id_in_str)
        position1_in_str = callback.data.split('_')[2]
        new_position = int(position1_in_str)
        position2_in_str = callback.data.split('_')[3]
        old_position = int(position2_in_str)

        user1_id = await rq.get_user_id_by_position(queue_id, new_position)
        user2_id = await rq.get_user_id_by_position(queue_id, old_position)

        user1 = await rq.get_user_nickname(user1_id)
        user2 = await rq.get_user_nickname(user2_id)

        if await rq.switch_positions(queue_id, new_position, old_position):
            await callback.message.answer(f'{old_position} <- {user1}\n'
                                          f'{new_position} <- {user2}')
        else:
            await callback.message.answer(f'Error')
    else:
        await callback.message.answer(f'{callback.from_user.first_name}, u dnt hace access to this fnctn')


@router.callback_query(F.data.startswith('remove_'))
async def remove_selected(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if await admin_filter(user_id, chat_id):
        queue_id_str = callback.data.split('_')[1]
        queue_id = int(queue_id_str)
        user_id_str = callback.data.split('_')[2]
        user_id = int(user_id_str)
        queue_name = await rq.get_queue(queue_id)
        chat_id = callback.message.chat.id
        if not await rq.leave_queue(user_id, chat_id, queue_name):
            await callback.message.answer(f'{await rq.get_user_nickname(user_id)} has been removed from the {queue_name}')
        else:
            await callback.message.answer(f'{await rq.get_user_nickname(user_id)} were not in the queue {queue_name} anyway')
    else:
        await callback.message.answer(f'{callback.from_user.first_name}, u dnt hace access to this fnctn')


# @router.callback_query(F.data == '')
