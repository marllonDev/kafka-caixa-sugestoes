# Projeto Caixa de Sugestões (Backend)

Este projeto implementa o backend para um sistema de caixa de sugestões. Ele utiliza uma arquitetura de microsserviços orientada a eventos, com uma API para receber dados, uma fila de mensagens para processamento assíncrono e um banco de dados para persistência.

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework API:** Flask
* **Fila de Mensagens:** Apache Kafka (via imagem Bitnami)
* **Banco de Dados:** PostgreSQL
* **Containerização:** Docker & Docker Compose
* **Gerenciamento de Ambiente:** Venv
* **Front-end:** [link](https://github.com/marllonDev/sugestoes-app-flutter) OBS:Esse é um front-end em Flutter, mas não é obrigatrório, pois você pode fazer as requisições API pelo Postman por exemplo. Mas se quiser fazer direto pelo app, basta clica no link e seguir conforme orientado.

---

## Como Rodar o Projeto

### Pré-requisitos

* [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose instalados.
* Python 3.13 (ou superior estável) instalado e acessível no PATH do sistema.
* Um terminal compatível com Bash (como **Git Bash** no Windows, ou o terminal padrão no Linux/macOS).

### Guia de Instalação e Execução

Todo o processo de configuração do ambiente e inicialização da infraestrutura foi automatizado em um único script para facilitar.

#### Passo 1: Clone e Configure o Ambiente

Primeiro, clone o repositório e navegue para a pasta do projeto. Em seguida, crie o arquivo de configuração de ambiente.

Faça uma cópia do arquivo `.env.example` (se existir) ou crie um novo arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Configurações do Kafka
KAFKA_SERVER=localhost:9092
KAFKA_TOPIC=sugestoes-topic
KAFKA_CONSUMER_GROUP=grupo-sugestoes-arquivistas

# Configurações do Banco de Dados PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sugestoes_db
DB_USER=dev
DB_PASSWORD=kafka
```

#### Passo 2: Execute o Script de Inicialização

No seu terminal (use Git Bash se estiver no Windows), execute o script `start-backend.sh`.

```bash
sh start-backend.sh
```

Este script fará o seguinte, automaticamente:
1.  Criará um ambiente virtual Python na pasta `.venv` (se não existir).
2.  Ativará o ambiente virtual.
3.  Instalará todas as dependências listadas em `requirements.txt`.
4.  Iniciará os contêineres do Kafka e PostgreSQL com `docker-compose`.
5.  Criará a tabela `sugestoes` no banco de dados.

#### Passo 3: Rode os Serviços Python

Após a execução bem-sucedida do script, seu ambiente estará pronto. Agora você precisa iniciar os dois serviços Python em **terminais separados**.

* **Terminal 1 - Inicie a API:**
    * *Primeiro, ative o ambiente virtual neste terminal: `source .venv/Scripts/activate` ou `source .venv/bin/activate` para Linux e Mac*
    * *Depois, rode o script:*
    ```bash
    python run_api.py
    ```

* **Terminal 2 - Inicie o Consumidor:**
    * *Primeiro, ative o ambiente virtual neste terminal: `source .venv/Scripts/activate` ou `source .venv/bin/activate` para Linux e Mac*
    * *Depois, rode o script:*
    ```bash
    python run_consumer.py
    ```

## Endpoints da API

Com o backend rodando, você pode interagir com os seguintes endpoints:

### 1. Enviar uma Nova Sugestão

* **Método:** `POST`
* **URL:** `http://localhost:5000/sugestao`
* **Corpo (Body):** JSON

**Exemplo com `curl`:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"autor": "Marlla", "sugestao": "Adicionar mais exemplos no README!"}' http://localhost:5000/sugestao
```

**Exemplo para Postman (ou similar):**
1.  Defina o método como `POST`.
2.  Insira a URL: `http://localhost:5000/sugestao`.
3.  Vá para a aba `Body`, selecione a opção `raw` e o tipo `JSON`.
4.  Insira o conteúdo no corpo da requisição:
    ```json
    {
        "autor": "Usuario de Postman",
        "sugestao": "Esta sugestão veio do Postman."
    }
    ```
5.  Clique em "Send".

### 2. Buscar Todas as Sugestões

* **Método:** `GET`
* **URL:** `http://localhost:5000/sugestoes`

**Exemplo com `curl`:**
```bash
curl -X GET http://localhost:5000/sugestoes
```

**Exemplo para Postman (ou similar):**
1.  Defina o método como `GET`.
2.  Insira a URL: `http://localhost:5000/sugestoes`.
3.  Clique em "Send".

A resposta será uma lista em formato JSON com todas as sugestões salvas no banco de dados.

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

## Sobre mim
𝐒𝐞𝐧𝐢𝐨𝐫 𝐃𝐚𝐭𝐚 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫

Com 𝟰+ 𝘆𝗲𝗮𝗿𝘀 de experiência no mundo da tecnologia, eu me desenvolvo na interseção entre engenharia de dados e inovação. Atualmente, estou criando ecossistemas de dados escaláveis como 𝗦𝗲𝗻𝗶𝗼𝗿 𝗗𝗮𝘁𝗮 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿. Aperfeiçoei minhas habilidades em setores que moldam as economias - desde 𝗺𝗮𝗶𝗼𝗿𝗲𝘀 𝗯𝗮𝗻𝗰𝗼𝘀 𝗱𝗼 𝗕𝗿𝗮𝘀𝗶𝗹 e 𝘀𝗲𝗴𝘂𝗿𝗮𝗱𝗼𝗿𝗮𝘀 𝗹𝗶𝗱𝗲𝗿𝗲𝘀 𝗺𝘂𝗻𝗱𝗶𝗮𝗶𝘀, até o 𝗺𝗮𝗶𝗼𝗿 𝗽𝗿𝗼𝗱𝘂𝘁𝗼𝗿 𝗱𝗲 𝗰𝗲𝗿𝘃𝗲𝗷𝗮 do mundo, e agora estou causando impacto no 𝘀𝗲𝘁𝗼𝗿 𝗱𝗼 𝗰𝗿𝗲𝗱𝗶𝘁𝗼. 

💡 𝗣𝗼𝗿𝗾𝘂𝗲 𝗲𝘂 𝗺𝗲 𝗱𝗲𝘀𝘁𝗮𝗰𝗼? \
Eu 𝗮𝗿𝗾𝘂𝗶𝘁𝗲𝘁𝗼 𝗽𝗶𝗽𝗲𝗹𝗶𝗻𝗲𝘀 de dados robustos para 𝗙𝗼𝗿𝘁𝘂𝗻𝗲 𝟱𝟬𝟬 𝗽𝗹𝗮𝘆𝗲𝗿𝘀, otimizei os sistemas legados para nuvem (𝗔𝗪𝗦/𝗔𝘇𝘂𝗿𝗲) que forneceram insights acionáveis por meio de estruturas ETL/ELT escaláveis. Da análise financeira em tempo real à otimização da cadeia de suprimentos de cervejarias, eu transformo dados brutos em ativos estratégicos. 

✨ 𝗔𝗹𝗲𝗺 𝗱𝗼 𝗰𝗼𝗱𝗶𝗴𝗼: \
Um aprendiz permanente obcecado com a democratização de dados e a solução ágil de problemas. Vamos nos conectar se você estiver 𝗮𝗽𝗮𝗶𝘅𝗼𝗻𝗮𝗱𝗼 sobre a nuvem, eficiência do 𝗗𝗲𝘃𝗢𝗽𝘀 ou o papel dos dados na transformação dos setores!

Me siga: [Linkedin](https://www.linkedin.com/in/marllonzuc/) \
Meu Blog: [Blog](https://datatrends.me/)

![Logo](https://media.licdn.com/dms/image/v2/D4D03AQEFlFTNmApBhQ/profile-displayphoto-shrink_800_800/B4DZbt9iTrHsAc-/0/1747749054334?e=1756944000&v=beta&t=NW8glGWRr3nju_eTn_S49tng936yy-t1pxHxTU0JZ38)
