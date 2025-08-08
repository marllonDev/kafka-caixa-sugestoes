import json
import time
import psycopg2
from kafka import KafkaConsumer


TOPIC_NAME = 'sugestoes-topic' # Nome do tópico que vamos "ouvir"
GROUP_ID = 'grupo-sugestoes-arquivistas' # ID do grupo de consumidores para nossa "equipe de operários"
BOOTSTRAP_SERVERS = 'localhost:9092' # Endereço do nosso servidor Kafka (agora acessível do seu PC)
DB_HOST = "localhost" # Usamos o nome localhost pois esse consumidor roda neste PC, não em um contâiner docker
DB_PORT = "5432"
DB_NAME = "sugestoes_db"
DB_USER = "dev"
DB_PASSWORD = "kafka"

print("➡️  Iniciando Consumidor Kafka...")
print(f"   Tópico: {TOPIC_NAME}")
print(f"   Grupo de Consumidores: {GROUP_ID}")

# --- 1. Inciando Consumidor ---
consumer = None
for i in range(5):
    try:
        # Instanciamos o Consumidor
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            auto_offset_reset='earliest', # Começa a ler desde a mensagem mais antiga
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("✅ Consumidor Kafka conectado com sucesso!")
        break
    except Exception as e:
        print(f"❌ Tentativa {i+1}/5 falhou. Erro ao conectar com o Kafka: {e}")
        time.sleep(5)


# --- 2. Conexão com o Banco de Dados ---
db_conn = None
if consumer: # Só tenta conectar ao banco se o Kafka estiver ok
    try:
        # Usando a biblioteca psycopg2 para conectar ao nosso Postgres
        db_conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Conexão com o PostgreSQL estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar com o PostgreSQL: {e}")


# --- 3. Loop de Processamento ---

if not consumer or not db_conn:
    print("🚨 Encerrando o consumidor por falha na conexão com Kafka ou PostgreSQL.")
else:
    print("\n🎧 Ouvindo o tópico em busca de novas sugestões para salvar no banco...")
    try:
        for message in consumer:
            sugestao_data = message.value
            
            print("\n----------------------------------------------------")
            print(f"📬 Nova sugestão recebida do Kafka: {sugestao_data}")

            try:
                # Criamos um "cursor", que é o objeto que executa os comandos SQL
                cursor = db_conn.cursor()

                # Pega os dados do JSON. Usamos .get() para evitar erros se a chave não existir.
                autor = sugestao_data.get('autor', 'Anônimo') # Define 'Anônimo' como padrão
                sugestao_texto = sugestao_data.get('sugestao')

                if sugestao_texto: # Só insere se houver um texto de sugestão
                    # O comando SQL para inserir os dados na nossa tabela
                    sql = "INSERT INTO sugestoes (autor, sugestao) VALUES (%s, %s);"
                    
                    # Executando o comando de forma segura
                    # Passamos os valores como uma tupla para evitar SQL Injection
                    cursor.execute(sql, (autor, sugestao_texto))

                    # A transação no banco de dados precisa ser "commitada"
                    # para que a alteração seja salva permanentemente.
                    db_conn.commit()
                    
                    print(f"💾 Sugestão salva no banco de dados com sucesso!")
                
                # Fechamos o cursor após o uso
                cursor.close()

            except Exception as e:
                print(f"🔥 Erro ao salvar no banco de dados: {e}")
                # Em caso de erro, é uma boa prática reverter a transação
                db_conn.rollback()
            # --- FIM DA NOVA LÓGICA ---

    except KeyboardInterrupt:
        print("\n\n🔌 Desligando o consumidor...")
    finally:
        # Garante que as conexões sejam fechadas ao encerrar.
        if consumer:
            consumer.close()
        if db_conn:
            db_conn.close()
            print("❌ Conexão com o PostgreSQL fechada.")