# Exemplo 2: Containers Conversando Entre Si 
---

## 📁 Entendendo os Arquivos

### **app.py** - A Aplicação Web
```python
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='meu_banco', port=6379)

@app.get('/')
def home():
    # Incrementa o contador no Redis
    hits = redis.incr('contador')
    
    return f"""
    <html>
        <head>
            <style>
                body {{ background-color: #0d1117; color: white; display: flex; ... }}
                .box {{ border: 3px solid #009688; padding: 40px; border-radius: 20px; ... }}
                h1 {{ font-size: 3rem; color: #009688; }}
                span {{ font-size: 5rem; font-weight: bold; color: #ffa600; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1>Jornada da Informática</h1>
                <p>Este site já foi acessado</p>
                <span>{hits}</span>
                <p>vezes de dentro de um container!</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**O que este arquivo faz:**
- Importa `Flask` (framework web) e `Redis` (banco de dados em memória)
- Conecta ao Redis usando `host='meu_banco'` (nome do outro container!)
- A rota `/` incrementa um contador no Redis
- **Mostra um número que sobe a cada acesso**: 1, 2, 3, 4...

### **requirements.txt** - Dependências Python
```
flask
redis
```

**O que significa:**
- `flask`: Framework para criar a aplicação web
- `redis`: Biblioteca Python para se comunicar com o Redis (banco de dados)

### **Dockerfile** - A Receita da Imagem
```dockerfile
# 1. Começamos com uma imagem leve do Python
FROM python:3.9-slim

# 2. Definimos a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copiamos o arquivo de dependências primeiro (otimiza o cache)
COPY requirements.txt .

# 4. Instalamos o Flask e o cliente do Redis
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos o resto do código (app.py)
COPY . .

# 6. Informamos que o app roda na porta 5000
EXPOSE 5000

# 7. O comando para iniciar o app
CMD ["python", "app.py"]
```

**Explicação de cada linha:**

| Linha | O que faz | 
|-------|----------|
| `FROM python:3.9-slim` | Começa com Python pronto |
| `WORKDIR /app` | Define pasta de trabalho |
| `COPY requirements.txt .` | Copia arquivo de dependências |
| `RUN pip install...` | Instala Flask e Redis |
| `COPY . .` | Copia todo o código | |
| `EXPOSE 5000` | Documenta que a porta 5000 será usada |
| `CMD ["python", "app.py"]` | Comando que inicia o app |

### **docker-compose.yml** - O Maestro da Orquestração
```yaml
version: '3.8'

services:
  # Nosso app Flask
  web:
    build: .
    ports:
      - "5001:5000"
    volumes:
      - .:/app
    depends_on:
      - meu_banco

  # O Banco de Dados Redis
  meu_banco:
    image: "redis:alpine"
    restart: always
```

**Entendendo cada parte:**

#### **Serviço `web` (Aplicação)**
```yaml
web:
  build: .                    # Constrói a imagem do Dockerfile
  ports:
    - "5001:5000"           # Porto 5001 do PC → Porto 5000 do container
  volumes:
    - .:/app                 # Mapeia pasta local para /app do container
  depends_on:
    - meu_banco              # Espera o Redis iniciar antes
```

- `build: .`: "Construa a imagem usando o Dockerfile da pasta atual"
- `ports: "5001:5000"`: Você acessa em `localhost:5001`
- `volumes: .:/app`: Hot reload! Mudanças no código aparecem instantaneamente
- `depends_on`: "Só suba meu container DEPOIS que o Redis subir"

#### **Serviço `meu_banco` (Redis)**
```yaml
meu_banco:
  image: "redis:alpine"      # Usa a imagem Redis (baixada do Docker Hub)
  restart: always            # Se cair, reinicia automaticamente
```

- `image: "redis:alpine"`: Usa a imagem oficial do Redis (muito leve!)
- `restart: always`: **IMPORTANTE** - Se o container cai, reinicia sozinho!

---

## Reproduzindo exemplo - parte 1

### **Pré-requisitos**
- Docker e Docker Compose instalados
- Terminal aberto
- Estar dentro de `004-exemplo2/myapp2`

### **Passo 1: Navegue até a pasta**

```bash
cd /caminho/para/004-exemplo2/myapp2
```

### **Passo 2: Inicie os serviços com Docker Compose**

```bash
docker compose up -d
```

**O que está acontecendo:**
- `docker-compose up`: Inicia todos os serviços definidos no arquivo
- `-d`: Executa em "detached mode" (roda em segundo plano, libera seu terminal)

**Você verá:**
```
Creating myapp2_web_1       ... done
Creating myapp2_meu_banco_1 ... done
```

### **Passo 3: Verifique se tudo está rodando**

```bash
docker compose ps
```

Você verá:
```
NAME                    COMMAND                  SERVICE      STATUS
myapp2_web_1           "python app.py"          web          Up 2 seconds
myapp2_meu_banco_1      "redis-server"           meu_banco     Up 3 seconds
```

✅ Ambos estão **Up** (rodando)!

### **Passo 4: Abra no navegador**

1. Abra `http://localhost:5001`
2. Você verá:
   ```
   Jornada da Informática
   Este site já foi acessado
   1
   vezes de dentro de um container!
   ```

### **Passo 5: Atualize a Página Várias Vezes**

Pressione `F5` (ou `Cmd+R` no Mac) várias vezes:

```
1 → 2 → 3 → 4 → 5 → ...
```

O número sobe a cada atualização! 🎉

**O que está acontecendo nos bastidores:**
1. Seu navegador envia uma requisição HTTP para `localhost:5001`
2. O container `web` recebe a requisição
3. A aplicação Flask conecta no Redis (container `meu_banco`)
4. Redis incrementa o contador
5. Você vê o número novo

### **Passo 6: Veja os Logs em Tempo Real**

Abra outro terminal e execute:

```bash
docker compose logs -f web
```

Agora, toda vez que você atualizar a página, verá logs como:
```
web_1 | 172.19.0.1 - - [13/Jan/2026 10:35:20] "GET / HTTP/1.1" 200 -
web_1 | 172.19.0.1 - - [13/Jan/2026 10:35:22] "GET / HTTP/1.1" 200 -
```

> `Ctrl + C` para sair dos logs

---

## Reproduzindo exemplo - parte 2

Agora vamos demonstrar o **problema em um sistema tradicional vs a resiliência do Docker**.

### **Cenário: O Banco de Dados Cai**

#### **1. Mate o container do Redis**

```bash
docker compose stop meu_banco
```

Você verá:
```
Stopping myapp2_meu_banco_1 ... done
```

#### **2. Volte ao navegador e atualize**

Acesse `http://localhost:5001` novamente e pressione `F5`

**O que você verá:**
- A página fica **travada**
- O número **não sobe mais**
- Depois de alguns segundos, você vê um **erro 500**

#### **3. Veja o erro nos logs**

```bash
docker compose logs web
```

Você verá algo como:
```
web_1 | ConnectionError: Error 111 connecting to meu_banco:6379. Connection refused.
web_1 | Error: Connection pool is exhausted
```

#### **4. Agora vem a Mágica: Reinicie o Redis**

```bash
docker compose up -d
```

Apenas esse comando! Muito mais rápido:
```
Creating myapp2_meu_banco_1 ... done
```

#### **5. Volte ao Navegador**

Atualize a página em `http://localhost:5001`

**Veja a Mágica:**
- ✅ A página volta a funcionar!
- ✅ **O sistema se recuperou automaticamente!**

---