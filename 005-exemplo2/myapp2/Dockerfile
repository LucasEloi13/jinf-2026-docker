# 1. Começamos com uma imagem leve do Python
FROM python:3.9-slim

# 2. Definimos a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copiamos o arquivo de dependências primeiro (otimiza o cache)
# Criaremos esse arquivo no próximo passo
COPY requirements.txt .

# 4. Instalamos o Flask e o cliente do Redis
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos o resto do código (app.py)
COPY . .

# 6. Informamos que o app roda na porta 5000
EXPOSE 5000

# 7. O comando para iniciar o app
CMD ["python", "app.py"]