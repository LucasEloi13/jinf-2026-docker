 # Persistência de Dados com Docker

## Table of contents
<!-- no toc -->
- [I. Entendendo a persistência de dados](#i-entendendo-a-persistência-de-dados)
  - [A. Instalando dependências](#a-instalando-dependências)
  - [B. Persistindo dados produzidos pela aplicação](#b-persistindo-dados-produzidos-pela-aplicação)
    - [i. Volume Mounts](#i-volume-mounts)
    - [ii. Bind Mounts](#ii-bind-mounts)

---

## I. Entendendo a persistência de dados

Quando criamos um container a partir de uma imagem, **tudo que está na imagem é tratado como somente leitura (read-only)**.  
Sobre essa imagem, o Docker adiciona uma **nova camada de escrita (read/write)** específica daquele container.

![](./img/container-filesystem.jpg)

Isso significa que:
- A imagem nunca é modificada
- Qualquer alteração feita em tempo de execução fica **restrita ao container**
- Ao destruir o container, essa camada de escrita é perdida

---

### A. Instalando dependências

Vamos experimentar como funciona a instalação de algo **em tempo de execução** dentro de um container.

> ⚠️ **Nota:**  
> Modificar o conteúdo de um container em runtime **não é uma prática recomendada**.  
> Estamos fazendo isso **apenas para fins didáticos**.

```bash
# Criar um container a partir da imagem ubuntu
docker run --interactive --tty --rm ubuntu:22.04

# Tentar usar o ping
ping google.com -c 1
# Resultado: bash: ping: command not found

# Instalar o ping
apt update
apt install iputils-ping --yes

# Testar novamente
ping google.com -c 1 # Agora funciona!
exit
```

Vamos tentar novamente:
```bash
docker run -it --rm ubuntu:22.04
ping google.com -c 1# Falha novamente! 🤔
```

A segunda tentativa falhou porque instalamos o programa na camada de leitura/gravação específica do primeiro contêiner, e quando tentamos novamente, era um contêiner diferente com uma camada de leitura/gravação diferente!

Ou seja:
👉 Containers não compartilham estado por padrão.

Podemos dar um nome ao container para reutilizá-lo:
```bash
# Criar um container com nome (sem o --rm)
docker run -it --name my-ubuntu-container2 ubuntu:22.04

# Instalar e usar o ping
apt update
apt install iputils-ping --yes
ping google.com -c 1
exit


# Reiniciar o container e se conectar a ele
docker start my-ubuntu-container
docker attach my-ubuntu-container

# Testar o ping novamente
ping google.com -c 1 # Agora funciona! 🎉
exit
```

Apesar disso, nunca devemos depender de containers para persistir dados ou dependências.
O correto é incluir tudo o que a aplicação precisa dentro da imagem.

Instalando dependências corretamente (na imagem)
```bash
# Construir uma imagem baseada no ubuntu com o ping instalado
docker build --tag my-ubuntu-image -<<EOF
FROM ubuntu:22.04
RUN apt update && apt install iputils-ping --yes
EOF

# Criar um container a partir da imagem
docker run -it --rm my-ubuntu-image

# Confirmar que o ping já está disponível
ping google.com -c 1 # Sucesso! 🥳
```

As instruções `FROM` e `RUN` fazem parte de um arquivo chamado Dockerfile, que define como a imagem deve ser construída.

> 📌 Regra geral:
> Tudo que a aplicação precisa em runtime deve estar na imagem.

A única exceção são:
- Variáveis de ambiente
- Arquivos de configuração
- Credenciais específicas do ambiente

### B. Persistindo dados produzidos pela aplicação

Muitas aplicações produzem dados que precisam sobreviver ao ciclo de vida do container, como:
- Dados de banco de dados
- Uploads de usuários
- Arquivos gerados pela aplicação
Para isso, o Docker oferece:
- Volumes
- Mounts

![](./img/volumes.jpg)

Esses mecanismos permitem que os dados:
- Persistam mesmo que o container seja destruído
- Sejam compartilhados entre containers

Os dados podem ser armazenados:
- Em um local gerenciado pelo Docker (volume mount)
- Em um diretório do sistema host (bind mount)
- Em memória (tmpfs mount, não ilustrado)

> ***NOTA:** `Tmpfs mount` não persiste dados após o container finalizar. Ele é útil para dados temporários e sensíveis (ex: credenciais),não para dados da aplicação.*

---

**Testando persistência sem volumes.**

```bash
# Criar um container
docker run -it --rm ubuntu:22.04

# Criar diretório e arquivo
mkdir my-data
echo "Hello from the container!" > /my-data/hello.txt

# Verificar arquivo
cat my-data/hello.txt
exit
```

Criando um novo container:

```bash
docker run -it --rm ubuntu:22.04
cat my-data/hello.txt
# Erro: No such file or directory
```

>📌 Resultado esperado:
>O arquivo não existe, pois o container anterior foi destruído.

#### i. Volume Mounts
Volumes permitem persistir dados de forma segura e desacoplada do container.

```bash
# Criar um volume nomeado
docker volume create my-volume

# Criar um container montando o volume
docker run -it --rm --mount source=my-volume,destination=/my-data/ ubuntu:22.04

# Sintaxe alternativa (mais curta)
docker run -it --rm -v my-volume:/my-data ubuntu:22.04

# Criar arquivo no volume
echo "Hello from the container!" > /my-data/hello.txt
cat my-data/hello.txt
exit
```

Criando um novo container com o mesmo volume:

```bash
docker run  -it --rm --mount source=my-volume,destination=/my-data/ ubuntu:22.04
cat my-data/hello.txt # Agora funciona! 
exit
```

Onde esses dados ficam armazenados? No linux isso seria em `/var/lib/docker/volumes`... mas lembre-se, no docker desktop, Docker roda em uma VM linux.

#### ii. Bind Mounts

Bind mounts permitem montar diretórios do host diretamente no container.

Com o terminal dentro da pasta ./002-persistencia-de-dados:
```bash
mkdir my-data

docker run -it --rm \
--mount type=bind,source="${PWD}"/my-data,destination=/my-data \
ubuntu:22.04

# Sintaxe alternativa
docker run -it --rm -v ${PWD}/my-data:/my-data ubuntu:22.04

echo "Hello from the container!" > /my-data/hello.txt

# O arquivo também existe no host
cat my-data/hello.txt
exit

```

Os bind mounts podem ser interessantes se você quiser ter fácil visibilidade dos dados armazenados, mas existem vários motivos descritos em https://docs.docker.com/storage/volumes/ (incluindo a velocidade, caso esteja executando o Docker Desktop no Windows/Mac) pelos quais os volumes são preferíveis.