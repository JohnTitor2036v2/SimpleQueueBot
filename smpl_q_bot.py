import logging
import itertools
from datetime import datetime
from typing import Final
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN: Final = 'SECRET'
BOT_USERNAME: Final = '@smpl_q_bot'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Queues
q = []
class CustomQueue:
    id_obj = itertools.count()

    def __init__(self, creation_time):
        self.ID = next(CustomQueue.id_obj)
        self.creation_time = creation_time


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def create_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    creation_time = update.message.date
    q.append(CustomQueue(creation_time))
    await update.message.reply_text("New Queue has been created.")

async def list_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    head_row = "id\tdate\n"
    queues = ""
    for i in range(0, len(q)):
        queues = queues + str(q[i].ID) + "\t" + str(q[i].creation_time) + "\n"
    text = head_row + queues
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("create_queue", create_queue))
    application.add_handler(CommandHandler("list_queue", list_queue))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
