FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Copia o certificado customizado (se houver)
COPY cacert.pem /app/cacert.pem
ENV SSL_CERT_FILE=/app/cacert.pem

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Sobrescreve o cacert.pem do certifi (opcional, mas recomendado)
RUN cp /app/cacert.pem $(python -c "import certifi; print(certifi.where())")

EXPOSE 8501

CMD ["streamlit", "run", "botWeb.py", "--server.address=0.0.0.0"]