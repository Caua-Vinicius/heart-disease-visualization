# Usa uma imagem mais leve do Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos essenciais
COPY requirements.txt .

# Instala dependências sem armazenar cache
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Comando de inicialização
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
