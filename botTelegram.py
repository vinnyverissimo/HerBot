from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.constants import ChatAction
from config import TELEGRAM_TOKEN
from indexing import cria_indice, busca_contexto
from chat_engine import resposta_bot

indice = cria_indice()


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá! Eu sou o HerBot. Envie-me suas perguntas!")


async def echo(update, context):
    user_message = update.message.text
    chat_id = update.effective_chat.id
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    contexto = busca_contexto(indice, user_message)
    resposta = resposta_bot(user_message, contexto)
    await context.bot.send_message(chat_id=chat_id, text=resposta)


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), echo))
    application.run_polling()


if __name__ == '__main__':
    main()
