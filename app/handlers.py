from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from instances_for_main import bot

import logging
import asyncio
import app.keyboards as kb
import app.database.new_request as rq
import app.admin as admin


router = Router()
# ALLOWED_USER = []
ALLOWED_USER = {}
QUEUE_NAME = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    group_type = message.chat.type
    group_id = message.chat.id
    group_name = message.chat.title
    user_id = message.from_user.id

    if not group_type == 'private':
        if await admin.admin_filter(user_id, group_id):
            keyboard = await kb.admin_main()
        else:
            keyboard = await kb.main()

        if not await rq.add_group(group_id, group_name, group_type):
            await message.answer(f"New chat added: {group_id}, {group_name}, {group_type}.")

        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=keyboard)
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=keyboard)

    else:
        if not await rq.add_user(message.from_user.id, message.from_user.first_name):
            await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=await kb.private_main())
        else:
            nickname = await rq.get_user_nickname(message.from_user.id)
            await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.private_main())


@router.callback_query(F.data == 'create_queue')
async def create_queue(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    logging.info(f"Received message: {user_id}, {ALLOWED_USER}")

    if user_id in ALLOWED_USER:
        if any(chat_info[0] == chat_id and chat_info[1] is None for chat_info in ALLOWED_USER[user_id]):
            await callback.message.reply("Previous queue has not been named yet. Please finish the previous queue in this group.")
            return
        else:
            ALLOWED_USER[user_id].append((chat_id, None))
    else:
        ALLOWED_USER[user_id] = [(chat_id, None)]

    QUEUE_NAME.clear()

    nickname = await rq.get_user_nickname(user_id)
    await callback.message.reply(f'{nickname}, enter queue name: [!name <queue_names>]')

    asyncio.create_task(queue_creation_timer(user_id, chat_id))


async def queue_creation_timer(user_id, chat_id):
    await asyncio.sleep(60)
    if user_id in ALLOWED_USER and any(
            chat_info[0] == chat_id and not chat_info[1] for chat_info in ALLOWED_USER[user_id]):
        ALLOWED_USER[user_id].pop()
        await bot.send_message(chat_id, 'Queue creation time has expired.')
    else:
        ALLOWED_USER[user_id].pop()


@router.message(Command('name', prefix='!'))
async def naming_queue(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    print(ALLOWED_USER)

    if user_id in ALLOWED_USER and any(
            chat_info[0] == chat_id and not chat_info[1] for chat_info in ALLOWED_USER[user_id]):
        text = message.text[len('!name '):]
        QUEUE_NAME.append(text)
        size: int = await bot.get_chat_member_count(chat_id)
        logging.info(f"Received message: {QUEUE_NAME[0]}")
        logging.info(f"Received message: {size}")
        await rq.add_queue(group_id=chat_id, queue_name=text, size=size)
        await message.answer(f"{text} has been added!")
        ALLOWED_USER[user_id][-1] = (chat_id, text)
        QUEUE_NAME.clear()
    elif user_id not in ALLOWED_USER:
        nickname = await rq.get_user_nickname(user_id)
        await message.answer(
            f'{nickname}, you do not have permission to create a queue or the queue already has a name')
    else:
        await message.answer('Press «Create Queue» to use this functionality')


# @router.callback_query(F.data == 'create_queue')
# async def create_queue(callback: CallbackQuery):
#     ALLOWED_USER.clear()
#     QUEUE_NAME.clear()
#     if len(ALLOWED_USER) == 0:
#         logging.info(f"Received message: {callback.from_user.id}")
#         ALLOWED_USER.append(callback.from_user.id)
#         await callback.message.reply('Enter queue name: [!name ______]')
#     else:
#         await callback.message.reply("Previous queue has not been named yet.")
#
#
# @router.message(Command('name', prefix='!'))
# async def naming_queue(message: Message):
#     logging.info(f"Received message: {message.text}")
#     logging.info(f"Received message: {ALLOWED_USER}")
#     if message.from_user.id == ALLOWED_USER[0] and len(QUEUE_NAME) == 0:
#         text = message.text[len('!name '):]
#         QUEUE_NAME.append(text)
#         size: int = await bot.get_chat_member_count(message.chat.id)
#         logging.info(f"Received message: {QUEUE_NAME[0]}")
#         logging.info(f"Received message: {size}")
#         await rq.add_queue(group_id=message.chat.id, queue_name=text, size=size)
#         await message.answer(f"{QUEUE_NAME[0]} has been added!")
#         ALLOWED_USER.clear()
#         QUEUE_NAME.clear()
#     else:
#         await message.answer("You are not allowed to name the queue.")


@router.callback_query(F.data == 'show_queue')
async def show(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    await callback.message.answer('Select a queue to see more information', reply_markup=await kb.show_queue(chat_id))


@router.callback_query(F.data.startswith('show_'))
async def show_selected(callback: CallbackQuery):
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)
    positions = await rq.get_positions(queue_id)
    queue_name = await rq.get_queue(queue_id)

    pos_to_nick = {}

    for position in positions:
        user_id = position.user_id
        user_position = position.user_position
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
    await callback.message.answer('Select a queue to join', reply_markup=await kb.join_queue(chat_id))


@router.callback_query(F.data.startswith('join_'))
async def join_selected(callback: CallbackQuery):
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)
    queue_name = await rq.get_queue(queue_id)

    user_id = callback.from_user.id
    username = callback.from_user.first_name
    await rq.add_user(user_id, username)

    chat_id = callback.message.chat.id
    if not await rq.join_queue(user_id, chat_id, queue_name):
        await callback.message.answer(f'{username} follows the queue {queue_name}')
    else:
        await callback.message.answer(f'{username} already follows the queue {queue_name}')


@router.callback_query(F.data == 'leave_queue')
async def leave(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    await callback.message.answer('Select a queue to leave', reply_markup=await kb.leave_queue(chat_id))


@router.callback_query(F.data.startswith('leave_'))
async def leave_selected(callback: CallbackQuery):
    queue_id_str = callback.data.split('_')[1]
    queue_id = int(queue_id_str)
    queue_name = await rq.get_queue(queue_id)
    user_id = callback.from_user.id
    if not await rq.leave_queue(user_id, queue_id):
        await callback.message.answer(f'{callback.from_user.first_name} left the queue {queue_name}')
    else:
        await callback.message.answer(f'{callback.from_user.first_name} were not in the queue {queue_name} anyway')


@router.callback_query(F.data == 'delete_queue')
async def delete_selected(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer('To use this command write: [!delete <queue_name>]')


@router.message(Command('delete', prefix='!'))
async def delete(message: Message):
    chat_id = message.chat.id
    queue_name = message.text[len('!delete '):]
    queue_id = await rq.get_queue_id(chat_id, queue_name)
    if not await rq.delete_queue(queue_id):
        await message.answer(f"The queue {queue_name} was not found.")
    else:
        await message.answer(f"The queue {queue_name} has been deleted.")


# @router.callback_query(F.data == 'delete_queue')
# async def delete(callback: CallbackQuery):
#     chat_id = callback.message.chat.id
#     await callback.message.answer('Select a queue to delete', reply_markup=await kb.delete_queue(chat_id))
#
#
# @router.callback_query(F.data.startswith('delete_'))
# async def delete_selected(callback: CallbackQuery):
#     queue_id_str = callback.data.split('_')[1]
#     queue_id = int(queue_id_str)
#     queue_name = await rq.get_queue(queue_id)
#
#     if await rq.delete_queue(queue_id):
#         await callback.message.answer(f"The queue {queue_name} has been deleted.")
#     else:
#         await callback.message.answer(f"The queue {queue_name} was not found.")
