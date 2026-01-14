# Exemplo 1: Sua Primeira Aplicação com Docker 🚀

> Este exemplo mostra como empacotar uma **aplicação web simples** dentro de um container Docker, tornando-a portável e fácil de executar em qualquer computador.

## 📚 Entendendo o Conceito

Imagine que você tem uma receita de bolo (o código da sua aplicação). Quando você quer servir esse bolo:

1. **Sem Docker**: Você precisa ter a cozinha inteira instalada no seu computador (Python instalado, todas as bibliotecas necessárias, etc). Se o bolo ficar pronto, você o come. Mas se alguém quiser o mesmo bolo, precisa montar outra cozinha!

2. **Com Docker**: Você coloca a receita + a cozinha inteira em uma caixa (imagem). Quando quer comer, abre uma caixa (cria um container). A caixa já tem tudo necessário. Se alguém quer o mesmo bolo, abre outra caixa!

---

## 📁 Estrutura do Projeto

Antes de começar, conheça os arquivos que compõem este exemplo:

### **app.py** - A Aplicação
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Minha Palestra Docker</title>
            <style>
                body { background-color: #003f5c; color: white; display: flex; ... }
                h1 { font-size: 5rem; border: 5px solid #ffa600; ... }
            </style>
        </head>
        <body>
            <h1>🐳 Olá, Jornada da Informática!</h1>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**O que esse arquivo faz:**
- Cria uma aplicação web simples usando Flask (um framework Python para fazer websites)
- Define uma rota `/` (quando você acessa o site, ele retorna uma página HTML)
- Inicia o servidor na porta 5000
- O `host='0.0.0.0'` significa que o servidor está acessível de qualquer lugar

### **requirements.txt** - Dependências
```
flask
```

**O que isso significa:**
- Este arquivo lista as bibliotecas Python que nossa aplicação precisa
- No nosso caso, só precisamos do Flask (framework para fazer websites)
- Quando instalamos via `pip install -r requirements.txt`, Python baixa e instala tudo o que está listado aqui

### **Dockerfile** - A Receita
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Linha por linha:**

| Comando | O que faz |
|---------|----------|
| `FROM python:3.10-slim` | Começa com uma imagem Python já pronta |
| `WORKDIR /app` | Define `/app` como a pasta de trabalho dentro do container |
| `COPY requirements.txt .` | Copia o arquivo requirements.txt para dentro do container |
| `RUN pip install -r requirements.txt` | Instala as dependências (Flask) |
| `COPY . .` | Copia todo o código da aplicação |
| `CMD ["python", "app.py"]` | Define o comando que será executado quando o container iniciar |

### **docker-compose.yml** - O Orquestrador
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5001:5000"
    depends_on:
      - db

  db:
    image: mysql:8.4
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: minha_base
      MYSQL_USER: user
      MYSQL_PASSWORD: user123
    ports:
      - "3306:3306"
    volumes:
      - dbdata:/var/lib/mysql

volumes:
  dbdata:
```

**O que este arquivo faz:**
- Define os serviços que precisam rodar junto (nossa aplicação web e um banco de dados MySQL)
- Mapeia as portas para que você possa acessar de fora
- Define variáveis de ambiente (configurações do banco de dados)
- Persiste os dados do banco de dados em um volume
- O `depends_on: db` garante que o banco suba antes da aplicação

**Entendendo o mapeamento de portas:**
- `"5001:5000"` significa: a porta 5001 do seu computador direciona para a porta 5000 do container
- Dessa forma, você acessa a aplicação em `localhost:5001`

---

## 🚀 Passo a Passo - Reproduza Agora!

### **Pré-requisitos**
- Docker instalado no seu computador
- Terminal/Prompt de Comando aberto
- Estar dentro da pasta `003-exemplo1/myapp`

### **Passo 1: Abra o Terminal**

Abra o terminal/prompt de comando no seu computador e navegue até a pasta do projeto:

```bash
cd /caminho/para/003-exemplo1/myapp
```

> **Dica**: Se você está no Windows, use `cd C:\caminho\para\003-exemplo1\myapp`

### **Passo 2: Construa a Imagem Docker**

Agora vamos "montar a cozinha" (criar a imagem):

```bash
docker build -t minha-app:v1 .
```

**O que está acontecendo:**
- `docker build`: Constrói uma imagem Docker baseada no Dockerfile
- `-t minha-app:v1`: Nomeia a imagem como "minha-app" com versão "v1"
- `.`: Procura pelo Dockerfile na pasta atual

**Você verá algo como:**
```
[1/5] FROM python:3.10-slim
[2/5] WORKDIR /app
[3/5] COPY requirements.txt .
[4/5] RUN pip install -r requirements.txt
[5/5] COPY . .
Successfully built abc123def456
Successfully tagged minha-app:v1
```

### **Passo 3: Execute o Container**

Agora vamos "fatiar o bolo" (criar um container):

```bash
docker run -p 5001:5000 minha-app:v1
```

**O que está acontecendo:**
- `docker run`: Cria e inicia um novo container
- `-p 5001:5000`: Mapeia a porta 5000 do container para 5001 do seu computador
- `minha-app:v1`: Usa a imagem que construímos no passo anterior

**Você verá algo como:**
```
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server. Do not use it in production deployment.
```

### **Passo 4: Acesse a Aplicação no Navegador**

1. Abra seu navegador (Chrome, Firefox, Safari, Edge)
2. Vá para: `http://localhost:5001`
3. Você deve ver uma página com "🐳 Olá, Jornada da Informática!"

### **Passo 5: Veja o Servidor Respondendo**

Volte ao terminal onde você executou o `docker run`. Você verá logs como:

```
127.0.0.1 - - [13/Jan/2026 10:30:45] "GET / HTTP/1.1" 200 -
```

Isso significa:
- `127.0.0.1`: Seu próprio computador acessou
- `GET /`: Requisição HTTP GET para a raiz do site
- `200`: Resposta bem-sucedida (OK)

### **Passo 6: Pare o Container**

No terminal onde o container está rodando, pressione:

```
CTRL + C
```

Você verá:
```
Keyboard interrupt received, quitting.
```

---

## 🎯 Usando Docker Compose (Mais Fácil!)

Em vez de rodar o `docker build` e depois `docker run` separadamente, o Docker Compose faz tudo de uma vez!

### **Passo 1: Certifique-se de estar na pasta correta**

```bash
cd /caminho/para/003-exemplo1/myapp
```

### **Passo 2: Inicie os serviços com Compose**

```bash
docker-compose up
```

**O que está acontecendo:**
- Docker lê o arquivo `docker-compose.yml`
- Constrói a imagem (se necessário)
- Cria e inicia DOIS containers: `web` (nossa aplicação) e `db` (MySQL)
- Mostra os logs de ambos em tempo real

**Você verá algo como:**
```
Creating 003-exemplo1_web_1 ... done
Creating 003-exemplo1_db_1  ... done
Attaching to 003-exemplo1_web_1, 003-exemplo1_db_1
web_1  | Running on http://0.0.0.0:5000
db_1   | 2026-01-13 10:30:45 0 [Note] ready for connections
```

### **Passo 3: Acesse a aplicação**

1. Abra o navegador em `http://localhost:5001`
2. Você verá a mesma página de antes
3. O terminal mostrará os logs quando você acessar:
   ```
   web_1 | 127.0.0.1 - - [13/Jan/2026 10:30:50] "GET / HTTP/1.1" 200 -
   ```

### **Passo 4: Pare os serviços**

No terminal, pressione:
```
CTRL + C
```

Você verá:
```
Killing 003-exemplo1_web_1  ... done
Killing 003-exemplo1_db_1   ... done
```

Ambos os containers foram parados graciosamente.

### **Passo 5 (Opcional): Limpe tudo**

Para remover os containers e a rede:

```bash
docker-compose down
```

Você verá:
```
Removing 003-exemplo1_web_1 ... done
Removing 003-exemplo1_db_1  ... done
Removing network 003-exemplo1_default
```

---

## 🔍 Explorando Mais

### **Ver containers rodando**

```bash
docker ps
```

Mostra algo como:
```
CONTAINER ID   IMAGE         COMMAND              PORTS                  NAMES
abc123def456   minha-app:v1  "python app.py"      0.0.0.0:5001->5000/tcp my-container
```

### **Ver todos os containers (inclusive os parados)**

```bash
docker ps -a
```

### **Ver as imagens disponíveis**

```bash
docker images
```

Mostra algo como:
```
REPOSITORY     TAG    IMAGE ID       CREATED        SIZE
minha-app      v1     abc123def456   2 minutes ago   190MB
python         3.10   xyz789abc123   2 weeks ago     900MB
```

### **Ver os logs de um container**

```bash
docker logs <CONTAINER_ID>
```

Substitua `<CONTAINER_ID>` pelo ID do seu container. Mostra todos os logs históricos.

### **Entrar dentro de um container rodando**

```bash
docker exec -it <CONTAINER_ID> /bin/bash
```

Isso abre um terminal dentro do container! Você pode:
- Explorar os arquivos: `ls -la`
- Ver as dependências: `pip list`
- Sair com: `exit`

---


### **Possível Erro: "Port 5001 is already in use"**
Outro processo está usando a porta 5001. Opções:
```bash
# Use outra porta
docker run -p 5002:5000 minha-app:v1
```