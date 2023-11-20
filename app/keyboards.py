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
    # ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='Create Queue')],
    #     [KeyboardButton(text='Join Queue')],
    #     [KeyboardButton(text='Leave Queue')],
    #     [KeyboardButton(text='Show Queue')],
    #     [KeyboardButton(text='Delete Queue')],
    # ], resize_keyboard=True)


async def private_main():
    main_kb = InlineKeyboardBuilder()
    main_kb.add(InlineKeyboardButton(text='All Queues', callback_data='all_queues'))
    main_kb.add(InlineKeyboardButton(text='Show Queue', callback_data='show_queue'))
    main_kb.add(InlineKeyboardButton(text='Leave Queue', callback_data='leave_queue'))
    return main_kb.adjust(2).as_markup()


async def create_queue():
    pass


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


async def all_queues():
    pass


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
