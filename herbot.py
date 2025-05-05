from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import time

_ = load_dotenv(find_dotenv())

# ou outro modelo de sua preferência
chat = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.2)


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


def carrega_pdf():
    caminho = 'files/BaseDadosShakes.pdf'
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento = documento + doc.page_content
    return documento


# Configuração da página Streamlit
st.set_page_config(page_title='HerBot Chat')
st.header("🤖Bem vindo ao Herbot", divider=True)

# Inicialização das mensagens na sessão
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

# Exibição das mensagens anteriores
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem['role']):
        st.markdown(mensagem['content'])

# Input do usuário
if prompt := st.chat_input("Faça sua pergunta:"):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.mensagens.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # Exibe um indicador de que o bot está "digitando"
    with st.chat_message('assistant'):
        typing_message = st.empty()  # Placeholder para a mensagem temporária
        typing_message.markdown("digitando...")

    # Carrega o PDF e obtém a resposta do bot
    documento = carrega_pdf()
    resposta = resposta_bot(st.session_state.mensagens, documento)

    # Substitui o indicador pela resposta final
    typing_message.markdown(resposta)

    # Adiciona a resposta do bot ao histórico
    st.session_state.mensagens.append(
        {'role': 'assistant', 'content': resposta})
