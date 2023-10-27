from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


from app.database.request import get_queues

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Help')],
    [KeyboardButton(text='Create Queue')],
    [KeyboardButton(text='Join Queue')],
    [KeyboardButton(text='Leave Queue')],
    [KeyboardButton(text='Show Queue')],
    [KeyboardButton(text='Delete Queue')]
], resize_keyboard=True, input_field_placeholder='Choose a command')


async def help_keyboard_button():
    pass
    # await bot.send_message(
    #     chat_id=update.effective_message.chat_id,
    #     text='/createqueue - Create new queue\n'
    #         '/joinqueue - join to exist queue\n'
    #         '/showqueue - show all exist queue\n'
    #         '/leavequeue - leave exist queue\n'
    #         '/deletequeue - delete exist queue',
    #     reply_markup=main
    # )


async def create_queue_keyboard_button():
    pass


async def join_queue_keyboard_button():
    pass


async def leave_queue_keyboard_button():
    pass


async def show_queue_keyboard_button():
    queues_ikb = InlineKeyboardBuilder()
    queues = await get_queues()
    for queue in queues:
        queues_ikb.add(InlineKeyboardButton(text=queue.queue_name, callback_data=f'queue_{queue.id}'))
    return queues_ikb.adjust(2).as_markup()


async def delete_queue_keyboard_button():
    pass
