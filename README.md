# HerBot Telegram

HerBot é um assistente virtual que responde perguntas sobre documentos PDF utilizando IA generativa (RAG) e integração com o Telegram.

## Funcionalidades

- Lê e indexa automaticamente todos os arquivos PDF do diretório `files/`
- Recupera trechos relevantes dos documentos para responder perguntas (RAG)
- Integração com o Telegram Bot (responde em tempo real)
- Indicador de "digitando" enquanto processa a resposta

## Estrutura do Projeto

```
herbot_old/
│
├── bot.py                # Inicialização do bot e handlers do Telegram
├── chat_engine.py        # Função de geração de resposta (integração com LLM)
├── config.py             # Configurações e variáveis de ambiente
├── indexing.py           # Funções de indexação e busca de contexto (RAG)
├── requirements.txt      # Dependências do projeto
├── files/                # PDFs e outros arquivos de dados
└── README.md             # Este arquivo
```

## Como rodar o projeto

1. **Clone o repositório e instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz do projeto com:
     ```
     TELEGRAM_TOKEN=seu_token_aqui
     OPENAI_API_KEY=sua_openai_key_aqui
     ```

3. **Adicione seus arquivos PDF na pasta `files/`.**

4. **Execute o bot:**
   ```bash
   python bot.py
   ```

5. **No Telegram, envie mensagens para o seu bot e receba respostas baseadas nos PDFs!**

## Observações

- O bot utiliza o modelo `gpt-4o-mini` da OpenAI por padrão.
- O contexto é recuperado dinamicamente dos PDFs, tornando o sistema eficiente mesmo com grandes volumes de dados.
- Para dúvidas ou melhorias, abra uma issue ou envie um pull request.

---

Feito com 💚 por Vinny e IA.