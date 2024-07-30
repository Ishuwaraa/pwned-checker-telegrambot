import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder
from password_checker import pwned_check

load_dotenv()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey there! Send me a password to check if it has been pwned.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi there! 🌟 Just send me a password, "
                                    "and I'll check if it has been compromised in any known data breaches. "
                                    "It's a quick and easy way to see how many times your password has been pwned. "
                                    "Stay safe online!\nsource: https://haveibeenpwned.com")


def handle_response(text: str) -> str:
    password = text.lower().split()[0]
    return pwned_check(password)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User: {update.message.chat.id} in {message_type}: "{text}"')

    if message_type == 'group':
        # cuz in groups, bot can be called as @botname message
        if os.getenv('BOT_USERNAME') in text:
            new_text: str = text.replace(os.getenv('BOT_USERNAME'), '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    # command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    # app.add_error_handler(handle_error)

    # polls
    print('Polling...')
    app.run_polling(poll_interval=5)
