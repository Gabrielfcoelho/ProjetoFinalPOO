# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o container
COPY . .

# Exponha a porta 5000 (onde o Flask vai rodar)
EXPOSE 5000

# Defina o comando para iniciar a aplicação Flask
CMD ["python", "run.py"]
