from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


from app.database.request import get_queues, add_queue


async def main():
    main_kb = InlineKeyboardBuilder()
    main_kb.add(InlineKeyboardButton(text='Create Queue', callback_data='create_queue'))
    main_kb.add(InlineKeyboardButton(text='Join Queue', callback_data='join_queue'))
    main_kb.add(InlineKeyboardButton(text='Leave Queue', callback_data='leave_queue'))
    main_kb.add(InlineKeyboardButton(text='Show Queue', callback_data='show_queue'))
    main_kb.add(InlineKeyboardButton(text='Delete Queue', callback_data='delete_queue'))
    return main_kb.adjust(2).as_markup()


async def create_queue():
    pass


async def join_queue():
    pass


async def leave_queue():
    pass


async def show_queue():
    queues_kb = InlineKeyboardBuilder()
    queues = await get_queues()
    for queue in queues:
        queues_kb.add(InlineKeyboardButton(text=queue.queue_name, callback_data=f'queue_{queue.id}'))
    return queues_kb.adjust(2).as_markup()


async def delete_queue_keyboard_button():
    pass
