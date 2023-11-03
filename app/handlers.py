from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from tabulate import tabulate

import app.keyboards as kb
import app.database.request as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if not await rq.add_user(message.from_user.id, message.from_user.first_name):
        await message.answer(f'Welcome, {message.from_user.first_name}', reply_markup=await kb.main())
    else:
        nickname = await rq.get_user_nickname(message.from_user.id)
        await message.answer(f'Welcome back, {nickname}!', reply_markup=await kb.main())


# @router.message(Command('showqueue'))
# async def cmd_show_all(message: Message):
#     queues = await rq.get_queues()
#     await message.answer(queues)


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
