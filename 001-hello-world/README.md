## Hello World com Docker

<!-- - [A analogia do bolo 🍰](#a-analogia-do-bolo-)
- [O comando `docker run hello-world`](#o-comando-docker-run-hello-world)
- [O que acontece passo a passo](#o-que-acontece-passo-a-passo)
- [Analisando a saída do terminal linha por linha](#analisando-a-saída-do-terminal-linha-por-linha)
  - [Imagem não encontrada localmente](#imagem-não-encontrada-localmente)
  - [Download da imagem (pull)](#download-da-imagem-pull)
  - [Digest e verificação de integridade](#digest-e-verificação-de-integridade)
  - [Execução do container](#execução-do-container)
- [Quem são os personagens do Docker](#quem-são-os-personagens-do-docker)
- [Resumo mental (mapa rápido)](#resumo-mental-mapa-rápido) -->

---

## A analogia do bolo 

Vamos usar essa analogia durante **todo o material**:

| Conceito Docker | Analogia do bolo |
|-----------------|------------------|
| Dockerfile | Receita do bolo |
| Imagem | Bolo congelado |
| Container | Fatia do bolo servida |
| Registry (Docker Hub) | Doceria cheia de bolos |
| Docker Client | Você fazendo o pedido |
| Docker Daemon | A cozinha que prepara e serve |

---

## O comando `docker run hello-world`

```bash
docker run hello-world
```

---

## O que acontece passo a passo

Quando você executa:

```bash
docker run hello-world
```

O Docker faz exatamente isso:

1. O Docker Client recebe o comando (run)
2. Ele fala com o Docker Daemon
3. O Daemon procura a imagem hello-world localmente
4. Se não encontrar, vai até o Registry (Docker Hub)
5. Baixa a imagem
6. Cria um container
7. Executa o container

Tudo isso acontece em segundos.

![](./img/docker-architecture.png)

---

## Analisando a saída do terminal linha por linha

```bash
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
198f93fd5094: Pull complete 
Digest: sha256:d4aaab6242e0cace87e2ec17a2ed3d779d18fbfd03042ea58f2995626396a274
Status: Downloaded newer image for hello-world:latest
```

Ou seja:
- Você nunca baixou essa imagem antes
- O Docker ainda não tem o hello-world salvo localmente
- Vai no repositório oficial e baixa a imagem

--- 

## Execução do container

```bash
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Isso é a fatia do bolo sendo servida.

Tecnicamente:
- O Docker criou um container
- Executou um pequeno programa dentro dele
- Esse programa imprimiu essa mensagem
- O container encerrou automaticamente

---
