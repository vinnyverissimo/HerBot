from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

chat = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.2)
# chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.2)


def resposta_bot(pergunta, contexto, max_retries=3):
    mensagem_system = f'''Você é um assistente amigável chamado HerBot que responde perguntas no telegram. 
    Você só pode responder EXCLUSIVAMENTE com base no seguinte contexto: {contexto}.
    Sempre que possível, forneça respostas detalhadas, completas e explique de forma clara e didática.'''
    mensagens_modelo = [('system', mensagem_system), ('user', pergunta)]
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    import time
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
