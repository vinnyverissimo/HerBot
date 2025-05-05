import os
import time
from dotenv import load_dotenv, find_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.constants import ChatAction
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

_ = load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# ou outro modelo de sua preferência
chat = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.2)

# Função para carregar e indexar o PDF


def cria_indice():
    caminho = 'files/BaseDadosShakes.pdf'
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()

    # Divide o texto em partes menores para indexação
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=200)
    documentos = []
    for doc in lista_documentos:
        textos_divididos = text_splitter.split_text(doc.page_content)
        documentos.extend([Document(page_content=texto)
                          for texto in textos_divididos])

    # Cria o índice usando FAISS
    embeddings = OpenAIEmbeddings()  # Atualizado para usar o pacote correto
    indice = FAISS.from_documents(documentos, embeddings)
    return indice


# Inicializa o índice globalmente
indice = cria_indice()

# Função para buscar contexto relevante


def busca_contexto(pergunta):
    # Recupera os 3 trechos mais relevantes
    resultados = indice.similarity_search(pergunta, k=15)
    contexto = "\n".join([resultado.page_content for resultado in resultados])
    return contexto

# Função para gerar a resposta do bot


def resposta_bot(pergunta, max_retries=3):
    contexto = busca_contexto(pergunta)  # Busca o contexto relevante
    mensagem_system = f'''Você é um assistente amigável chamado HerBot que responde perguntas no telegram. 
    Você só pode responder EXCLUSIVAMENTE com base no seguinte contexto: {contexto}.
    Caso seja feita alguma pergunta fora do contexto, você deve se desculpar e dizer que não sabe responder.'''

    mensagens_modelo = [('system', mensagem_system), ('user', pergunta)]
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat

    for retry in range(max_retries):
        try:
            return chain.invoke({}).content
        except Exception as e:
            print(
                f"Erro na chamada da API (tentativa {retry + 1}/{max_retries}): {e}")
            if retry < max_retries - 1:
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

    # Envia a ação de "digitando" para o usuário
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Obtém a resposta do bot
    resposta = resposta_bot(user_message)

    # Envia a resposta final para o usuário
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
