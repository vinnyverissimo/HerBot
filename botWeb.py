import streamlit as st
import time
from indexing import cria_indice, busca_contexto
from chat_engine import resposta_bot

# Inicializa o índice globalmente (apenas uma vez)
if 'indice' not in st.session_state:
    st.session_state.indice = cria_indice()

st.set_page_config(page_title='HerBot Chat')
st.header("🤖 Bem-vindo ao HerBot", divider=True)

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
        typing_message = st.empty()
        typing_message.markdown("pensando...")

    # Busca contexto e obtém a resposta do bot
    contexto = busca_contexto(st.session_state.indice, prompt)
    resposta = resposta_bot(prompt, contexto)

    # Exibe a resposta aos poucos (efeito de digitação)
    displayed = ""
    for char in resposta:
        displayed += char
        typing_message.markdown(displayed)
        time.sleep(0.015)  # Ajuste a velocidade conforme desejar

    # Adiciona a resposta do bot ao histórico
    st.session_state.mensagens.append(
        {'role': 'assistant', 'content': resposta})
