from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
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
    if chat_type == 'supergroup' or chat_type == 'group':
        chat_id = message.chat.id
        chat_name = message.chat.title
        if not await rq.add_chat(chat_id, chat_name):
            await message.answer(f"New chat added: {chat_id}, {chat_name}.")
        else:
            await message.answer(f"Chat was already in db: {chat_id}, {chat_name}.")
        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=kb.main)
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=kb.main)
    else:
        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=await kb.private_main())
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.private_main())


@router.message(Command('showqueues'))
async def cmd_show_all(message: Message):
    queues = await rq.get_group_queues(message.chat.id)
    await message.answer(str(queues))


@router.callback_query(F.data == 'create_queue')
async def create_queue(message: Message):
    ALLOWED_USER.clear()
    if len(ALLOWED_USER) == 0:
        logging.info(f"Received message: {message.from_user.id}")
        ALLOWED_USER.append(message.from_user.id)
        await message.answer('Enter queue name: [!name ______]')
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
    chat_id = callback.message.chat.id
    await callback.message.answer('Choose a queue to see more information', reply_markup=await kb.show_queue(chat_id))


@router.callback_query(F.data.startswith('queue_'))
async def queue_selected(callback: CallbackQuery):
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)
    positions = await rq.get_positions(queue_id)
    queue_name = await rq.get_queue(queue_id)

    pos_to_nick = {}

    for position in positions:
        user_id = position.following_user_id
        user_position = position.position
        nickname = await rq.get_user_nickname(user_id)
        pos_to_nick[user_position] = nickname

    max_pos = await rq.get_queue_max_size(queue_id)
    output_lines = [f'{queue_name} positions:']
    for i in range(1, int(max_pos) + 1):
        nick = pos_to_nick.get(i, ' ')
        output_lines.append(f'{i}. {nick}')

    formatted_output = '\n'.join(output_lines)
    await callback.message.answer(formatted_output)


@router.callback_query(F.data == 'join_queue')
async def join(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    await callback.message.answer('Choose a queue to join', reply_markup=await kb.join_queue(chat_id))


@router.callback_query(F.data.startswith('join_'))
async def join_selected(callback: CallbackQuery):
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)
    queue_name = await rq.get_queue(queue_id)  # Retrieve the queue_name for the given queue_id
    user_id = callback.message.from_user.id
    chat_id = callback.message.chat.id
    await callback.message.answer('You here')
    if not await rq.join_queue(user_id, chat_id, queue_name):
        await callback.message.answer(f'You follow the queue {queue_name}')
    else:
        await callback.message.answer(f'You already follow the queue {queue_name}')

