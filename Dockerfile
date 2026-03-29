FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências primeiro (melhora o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código (incluindo a pasta static)
COPY . .

# Garante que as pastas necessárias existam dentro do contêiner
RUN mkdir -p static/uploads static/css static/img

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar o servidor
# Usamos 0.0.0.0 para que o contêiner aceite conexões de fora dele
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]