import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config import PDF_DIR


def cria_indice():
    documentos = []
    for nome_arquivo in os.listdir(PDF_DIR):
        if nome_arquivo.lower().endswith('.pdf'):
            caminho = os.path.join(PDF_DIR, nome_arquivo)
            loader = PyPDFLoader(caminho)
            lista_documentos = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200)
            for doc in lista_documentos:
                textos_divididos = text_splitter.split_text(doc.page_content)
                documentos.extend([Document(page_content=texto)
                                  for texto in textos_divididos])
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(documentos, embeddings)


def busca_contexto(indice, pergunta, k=15):
    resultados = indice.similarity_search(pergunta, k=k)
    return "\n".join([resultado.page_content for resultado in resultados])
