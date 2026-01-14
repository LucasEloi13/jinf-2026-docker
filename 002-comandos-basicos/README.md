# Comandos Básicos do Docker 🐳

---


### **Pré-requisitos**
- Docker instalado no computador
- Terminal/Prompt de comando aberto
- Conexão com a internet (para baixar a imagem)

---

## Passo 1: `docker pull` - Baixar uma Imagem

### O Comando
```bash
docker pull nginx
```

### O que faz?
Baixa a imagem `nginx` do Docker Hub (repositório oficial de imagens).

### Execute agora:
```bash
docker pull nginx
```

### Resultado esperado:
```
Using default tag: latest
latest: Pulling from library/nginx
e1436b96f6a3: Pull complete
40e319c3cd9f: Pull complete
82ee3a23a91f: Pull complete
Digest: sha256:1234567890abcdef...
Status: Downloaded newer image for nginx:latest
```

Aguarde até ver "Status: Downloaded" ou "Already exists" (se já tiver baixado antes).

---

## Passo 2: `docker images` - Verificar as Imagens Disponíveis

### O Comando
```bash
docker images
```

### O que faz?
Lista todas as imagens Docker que você tem no computador.

### Execute agora:
```bash
docker images
```

### Resultado esperado:
```
REPOSITORY     TAG      IMAGE ID       CREATED        SIZE
nginx          latest   1234567890ab   2 weeks ago    142MB
```

Você deve ver `nginx` na lista. Se tiver baixado outras imagens antes, elas também aparecerão aqui.

---

## Passo 3: `docker run` - Criar e Iniciar um Container

### O Comando
```bash
docker run -d -p 8080:80 nginx
```

### O que faz?
- `run`: Cria um novo container a partir da imagem `nginx`
- `-d`: Executa em segundo plano (detached mode)
- `-p 8080:80`: Mapeia a porta 8080 do seu computador para a porta 80 do container
- `nginx`: A imagem que será usada

### Execute agora:
```bash
docker run -d -p 8080:80 nginx
```

### Resultado esperado:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

Docker retorna um ID longo do container criado. Isso é normal.

---

## Passo 4: Abrir no Navegador - Ver o Nginx Funcionando

### O que fazer?
1. Abra seu navegador (Chrome, Firefox, Safari, Edge)
2. Digite na barra de endereços:
```
http://localhost:8080
```

### Resultado esperado:
Você verá uma página com "Welcome to nginx!" com informações do servidor.

**Parabéns!** Seu primeiro container está rodando! 🎉

---

## Passo 5: `docker ps` - Verificar Containers Rodando

### O Comando
```bash
docker ps
```

### O que faz?
Lista todos os containers que estão **rodando neste momento**.

### Execute agora:
```bash
docker ps
```

### Resultado esperado:
```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS        PORTS                 NAMES
a1b2c3d4e5f6   nginx     "nginx -g 'daemon of"   2 minutes ago   Up 2 minutes  0.0.0.0:8080->80/tcp eager_moore
```

Observe:
- `CONTAINER ID`: Identificador do seu container
- `STATUS`: "Up 2 minutes" significa que está rodando
- `PORTS`: Mostra o mapeamento de portas (8080->80/tcp)
- `NAMES`: Docker gerou um nome automático

**Seu container está funcionando!**

---

## Passo 6: `docker stop <container_id>` - Parar o Container

### O Comando
```bash
docker stop a1b2c3d4e5f6
```

Substitua `a1b2c3d4e5f6` pelo `CONTAINER ID` que você viu no passo anterior. Você pode copiar do resultado do `docker ps`.

### O que faz?
Para a execução do container graciosamente (ele tem tempo para se limpar).

### Execute agora:
Pegue o ID do seu container no passo anterior e execute:
```bash
docker stop <seu_container_id>
```

### Resultado esperado:
```
a1b2c3d4e5f6
```

Docker retorna o ID do container parado.

### Teste no navegador:
Tente acessar `http://localhost:8080` novamente.

**Resultado esperado:** 
- A página NÃO carrega
- Você vê um erro tipo "Connection refused" ou "This site can't be reached"

Isso significa que o container foi parado com sucesso!

---

## Passo 7: `docker ps -a` - Ver Containers Parados

### O Comando
```bash
docker ps -a
```

### O que faz?
Lista **todos** os containers: os que estão rodando E os que foram parados.

### Execute agora:
```bash
docker ps -a
```

### Resultado esperado:
```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS                   NAMES
a1b2c3d4e5f6   nginx     "nginx -g 'daemon of"   5 minutes ago   Exited (0) 1 minute ago  eager_moore
```

Observe:
- `STATUS`: Agora mostra "Exited (0)" em vez de "Up"
- O container ainda existe, está apenas parado

---

## Passo 8: `docker rm <container_id>` - Remover o Container

### O Comando
```bash
docker rm a1b2c3d4e5f6
```

Substitua `a1b2c3d4e5f6` pelo seu `CONTAINER ID`.

### O que faz?
Remove (deleta) o container completamente. Não é mais possível recuperá-lo.

### Execute agora:
```bash
docker rm <seu_container_id>
```

### Resultado esperado:
```
a1b2c3d4e5f6
```

Docker retorna o ID do container removido.

### Verificar:
Execute:
```bash
docker ps -a
```

**Resultado esperado:** O container não aparece mais em lugar nenhum!

---

## Passo 9: `docker images` - Verificar que a Imagem Ainda Existe

### O Comando
```bash
docker images
```

### O que faz?
Lista todas as imagens disponíveis.

### Execute agora:
```bash
docker images
```

### Resultado esperado:
```
REPOSITORY     TAG      IMAGE ID       CREATED        SIZE
nginx          latest   1234567890ab   2 weeks ago    142MB
```

A imagem `nginx` ainda está lá! Mesmo que tenhamos removido o container, a imagem permanece.

---

## Passo 10: `docker rmi nginx` - Remover a Imagem

### O Comando
```bash
docker rmi nginx
```

### O que faz?
Remove (deleta) a imagem `nginx` do computador. Libera espaço em disco.

### Execute agora:
```bash
docker rmi nginx
```

### Resultado esperado:
```
Untagged: nginx:latest
Deleted: sha256:1234567890ab...
Deleted: sha256:abcdef123456...
(pode mostrar mais "Deleted:" linhas)
```

### Verificar:
Execute:
```bash
docker images
```

**Resultado esperado:** A imagem `nginx` desapareceu da lista!

---

## 📋 Referência Rápida dos Comandos

| Passo | Comando | Resultado |
|-------|---------|-----------|
| 1 | `docker pull` | Baixa a imagem do Docker Hub |
| 2 | `docker images` | Mostra a imagem baixada |
| 3 | `docker run` | Cria um container rodando |
| 4 | (Navegador) `http://localhost:8080` | Vê o Nginx funcionando |
| 5 | `docker ps` | Vê o container rodando |
| 6 | `docker stop <id>` | Para o container |
| 7 | `docker ps -a` | Vê o container parado |
| 8 | `docker rm <id>` | Remove o container |
| 9 | `docker images` | Vê que a imagem ainda existe |
| 10 | `docker rm <id ou nome>` | Remove a imagem |
