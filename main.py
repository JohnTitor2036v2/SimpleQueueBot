import random
from typing import Final
from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

TOKEN: Final = 'Zhopa_Fili'
BOT_USERNAME: Final = '@simpleq_bot'

# Arrays

queues = {}


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/createqueue - Create new queue\n'
                                    '/joinqueue - join to exist queue\n'
                                    '/showqueue - show all exist queue\n'
                                    '/deletequeue - delete exist queue')


async def create_queue_command(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in queues:
        queues[chat_id] = []
        await update.message.reply_text('Queue created. Members can now join the queue using /joinqueue.')
    else:
        await update.message.reply_text('Queue already exists. Members can join the queue using /joinqueue.')


async def join_queue_command(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if chat_id in queues:
        if user_id not in queues[chat_id]:
            queues[chat_id].append(user_id)
            await update.message.reply_text('You have joined the queue.')
        else:
            await update.message.reply_text('You are already in the queue.')
    else:
        await update.message.reply_text('No queue exists. Create one using /createqueue.')


async def show_queue_command(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in queues and queues[chat_id]:
        queue = queues[chat_id]
        random.shuffle(queue)
        response = "Queue:\n"
        for index, user_id in enumerate(queue, start=1):
            user = await context.bot.get_chat_member(chat_id, user_id)
            response += f"{index} {user.user.first_name}\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text('No queue exists or the queue is empty.')


async def delete_queue_command(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in queues:
        del queues[chat_id]
        await update.message.reply_text('Queue deleted.')
    else:
        await update.message.reply_text('No queue exists to delete.')


# async def show_all_queues_command(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     if chat_id in queues:
#         response = "All Queues:\n"
#         for queue_name, users in queues[chat_id].items():
#             response += f"{queue_name} {len(users)}\n"
#         await update.message.reply_text(response)


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello there!'

    if 'test' in processed:
        return 'I`m fine'

    if 'tamer' in processed:
        return 'Gay'

    if 'tayir' in processed:
        return 'Я сосу черныечлена'

    if '' in processed:
        return ''

    return 'I can not understand you. Please, write correctly'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting work...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('createqueue', create_queue_command))
    app.add_handler(CommandHandler('joinqueue', join_queue_command))
    app.add_handler(CommandHandler('showqueue', show_queue_command))
    app.add_handler(CommandHandler('deletequeue', delete_queue_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
