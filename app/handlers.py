from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from tabulate import tabulate
from instances_for_main import bot

import logging
import app.keyboards as kb
import app.database.request as rq

router = Router()
ALLOWED_USER = []
QUEUE_NAME = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    chat_type = message.chat.type
    if chat_type == 'supergroup':
        chat_id = message.chat.id
        chat_name = message.chat.title
        if not await rq.add_chat(chat_id, chat_name):
            await message.answer(f"New chat added: {chat_id}, {chat_name}.")
        else:
            await message.answer(f"Chat was already in db: {chat_id}, {chat_name}.")
        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=await kb.main())
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.main())
    else:
        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=await kb.private_main())
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.private_main())

# # Command to retrieve the stored queue name
# @router.message(Command('get_queue_name'))
# async def cmd_get_queue_name(message: Message):
#     # Retrieve the user's queue name from the storage
#     user_id = message.from_user.id
#     user_data = await storage.get_data(chat=user_id)
#     queue_name = user_data.get('queue_name', 'No queue name saved yet.')

#     # Send the user's queue name
#     await message.answer(f"Your queue name is: {queue_name}")

@router.message(Command('showqueues'))
async def cmd_show_all(message: Message):
    queues = await rq.get_group_queues(message.chat.id)
    await message.answer(str(queues))

@router.message(Command('createqueue'))
async def create_queue(message: Message):
    if len(ALLOWED_USER) == 0:
        logging.info(f"Received message: {message.from_user.id}")
        ALLOWED_USER.append(message.from_user.id)
        await message.answer("Enter queue name: [!name ______]")
    else:
        await message.answer("Previous queue has not been named yet.")

@router.message()
async def naming_queue(message: Message):
    logging.info(f"Received message: {message.text}")
    logging.info(f"Received message: {ALLOWED_USER}")
    if '!name' in message.text:
        if message.from_user.id == ALLOWED_USER[0] and len(QUEUE_NAME) == 0:
            text = message.text[len('!name '):]
            QUEUE_NAME.append(text)
            ALLOWED_USER.clear()
            size: int = await bot.get_chat_member_count(message.chat.id)
            logging.info(f"Received message: {QUEUE_NAME[0]}")
            logging.info(f"Received message: {size}")
            await rq.add_queue(chat_id=message.chat.id, queue_name=text, size=size)
            await message.answer(f"{QUEUE_NAME[0]} has been added!")

@router.callback_query(F.data == 'show_queue')
async def queue(callback: CallbackQuery):
    await callback.message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue())


@router.callback_query(F.data.startswith('queue_'))
async def queue_selected(callback: CallbackQuery):
    queue_id = callback.data.split('_')[1]
    positions = await rq.get_positions(queue_id)
    queue_name = await rq.get_queue(queue_id)

    # Create a dictionary to map positions to nicknames
    pos_to_nickname = {}
    for position in positions:
        user_id = position.following_user_id
        pos = position.position
        nickname = await rq.get_user_nickname(user_id)
        pos_to_nickname[pos] = nickname

    # Generate the formatted output
    max_position = max(pos_to_nickname.keys(), default=0)
    output_lines = [f"{queue_name.queue_name} selected:"]
    for i in range(1, max_position + 1):
        nickname = pos_to_nickname.get(i, "*blank*")
        output_lines.append(f"{str(i)}. {nickname}")

    formatted_output = '\n'.join(output_lines)

    await callback.message.answer(formatted_output)
