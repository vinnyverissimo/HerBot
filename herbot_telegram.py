import os
import time
from dotenv import load_dotenv, find_dotenv
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

_ = load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# ou outro modelo de sua preferência
# chat = ChatOpenAI(model_name='gpt-4o-mini')
chat = ChatOpenAI(model_name='gpt-3.5-turbo-0125')


def carrega_pdf():
    caminho = 'files/BaseDadosShakes.pdf'
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento = documento + doc.page_content
    return documento


def resposta_bot(mensagens, documento, max_retries=3):
    mensagem_system = '''Você é um assistente amigável chamado HerBot. Você só pode responder EXCLUSIVAMENTE com base nessa fonte de dados: {informacoes}.
  Caso seja feita alguma pergunta fora do contexto, você deve se desculpar e dizer que não sabe'''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat

    for retry in range(max_retries):
        try:
            return chain.invoke({'informacoes': documento}).content
        except Exception as e:
            print(
                f"Erro na chamada da API (tentativa {retry + 1}/{max_retries}): {e}")
            if retry < max_retries - 1:
                # Espera exponencial antes de tentar novamente
                time.sleep(2 ** retry)
            else:
                return "Desculpe, não consegui obter uma resposta da API após várias tentativas."

# Função para lidar com comandos /start


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá! Eu sou o HerBot. Envie-me suas perguntas!")

# Função para lidar com mensagens de texto


async def echo(update, context):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    # Simula a estrutura de mensagens do Streamlit
    mensagens = [{'role': 'user', 'content': user_message}]

    # Carrega o PDF e obtém a resposta do bot
    documento = carrega_pdf()
    resposta = resposta_bot(mensagens, documento)

    await context.bot.send_message(chat_id=chat_id, text=resposta)

# Função principal para configurar e iniciar o bot


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Define os handlers: comandos e mensagens
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    # Inicia o bot
    application.run_polling()


if __name__ == '__main__':
    main()
