from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.database.request as rq


async def main():
    main_kb = InlineKeyboardBuilder()
    main_kb.add(InlineKeyboardButton(text='Create Queue', callback_data='create_queue'))
    main_kb.add(InlineKeyboardButton(text='Join Queue', callback_data='join_queue'))
    main_kb.add(InlineKeyboardButton(text='Leave Queue', callback_data='leave_queue'))
    main_kb.add(InlineKeyboardButton(text='Show Queue', callback_data='show_queue'))
    main_kb.add(InlineKeyboardButton(text='Delete Queue', callback_data='delete_queue'))
    return main_kb.adjust(2).as_markup()


async def admin_main():
    main_kb = InlineKeyboardBuilder()
    main_kb.add(InlineKeyboardButton(text='Create Queue', callback_data='create_queue'))
    main_kb.add(InlineKeyboardButton(text='Join Queue', callback_data='join_queue'))
    main_kb.add(InlineKeyboardButton(text='Leave Queue', callback_data='leave_queue'))
    main_kb.add(InlineKeyboardButton(text='Show Queue', callback_data='show_queue'))
    main_kb.add(InlineKeyboardButton(text='Delete Queue', callback_data='delete_queue'))
    main_kb.add(InlineKeyboardButton(text='Switch User Position', callback_data='switch_user_position'))
    main_kb.add(InlineKeyboardButton(text='Delete User Position', callback_data='delete_user_position'))
    return main_kb.adjust(2).as_markup()


async def private_main():
    main_kb = InlineKeyboardBuilder()
    main_kb.add(InlineKeyboardButton(text='All Queues', callback_data='all_queues'))
    main_kb.add(InlineKeyboardButton(text='Show Queue', callback_data='show_queue'))
    main_kb.add(InlineKeyboardButton(text='Leave Queue', callback_data='leave_queue'))
    return main_kb.adjust(2).as_markup()


async def join_queue(chat_id):
    queues_kb = InlineKeyboardBuilder()
    queues = await rq.get_queues(chat_id)
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=f'{queue.queue_name}', callback_data=f'join_{queue.id}'))
    return queues_kb.adjust(3).as_markup()


async def leave_queue(chat_id):
    queues_kb = InlineKeyboardBuilder()
    queues = await rq.get_queues(chat_id)
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=f'{queue.queue_name}', callback_data=f'leave_{queue.id}'))
    return queues_kb.adjust(3).as_markup()


async def show_queue(chat_id):
    queues_kb = InlineKeyboardBuilder()
    queues = await rq.get_queues(chat_id)
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=f'{queue.queue_name}', callback_data=f'show_{queue.id}'))
    return queues_kb.adjust(3).as_markup()


async def delete_queue(chat_id):
    queues_kb = InlineKeyboardBuilder()
    queues = await rq.get_queues(chat_id)
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=f'{queue.queue_name}', callback_data=f'delete_{queue.id}'))
    return queues_kb.adjust(3).as_markup()


async def switch_first_step(chat_id):
    queues_kb = InlineKeyboardBuilder()
    queues = await rq.get_queues(chat_id)
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=f'{queue.queue_name}', callback_data=f'first_{queue.id}'))
    return queues_kb.adjust(3).as_markup()


async def switch_second_step(queue_id):
    queues_kb = InlineKeyboardBuilder()
    positions = await rq.get_positions(queue_id)
    for position in positions:
        nickname = await rq.get_user_nickname(position.following_user_id)
        queues_kb.add(InlineKeyboardButton(
            text=f'{position.position}. {nickname}',
            callback_data=f'switch_{position.position}'
        ))
    return queues_kb.adjust(1).as_markup()
