import json
from kafka import KafkaConsumer
from . import config    # Importa as configurações
from . import database  # Importa nosso novo especialista em banco de dados

# --- Variável Global para o Consumidor ---
consumer = None

# --- Função de Inicialização ---
def initialize_consumer() -> bool:
    """
    Inicializa a conexão com o Kafka e cria a instância do consumidor.
    """
    global consumer
    try:
        # A instância do consumidor é criada aqui, usando as configurações centralizadas
        consumer = KafkaConsumer(
            config.KAFKA_TOPIC,
            bootstrap_servers=config.KAFKA_SERVER,
            group_id=config.KAFKA_CONSUMER_GROUP,
            auto_offset_reset='earliest', # Garante que leremos desde o início
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("✅ Consumidor Kafka inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar o consumidor Kafka: {e}")
        consumer = None
        return False

# --- Função Principal de Consumo ---
def start_consuming() -> None:
    """
    Inicia o loop principal do consumidor para processar mensagens.
    Esta função ficará rodando indefinidamente.
    """
    if not consumer:
        print("🚨 Consumidor Kafka não está disponível. Encerrando.")
        return

    print("\n🎧 Ouvindo o tópico em busca de novas sugestões para salvar...")
    try:
        # O loop infinito que espera por mensagens
        for message in consumer:
            sugestao_data = message.value
            
            print("\n----------------------------------------------------")
            print(f"📬 Nova sugestão recebida do Kafka: {sugestao_data}")

            # Em vez de ter toda a lógica SQL aqui, simplesmente delegamos
            # a tarefa para o nosso módulo especialista 'database'.
            # A função save_sugestao já contém toda a lógica de cursor,
            # INSERT, commit e rollback.
            database.save_sugestao(sugestao_data)
            print("----------------------------------------------------")

    except KeyboardInterrupt:
        # Ocorre quando pressionamos Ctrl+C no terminal
        print("\n\n🔌 Interrupção do usuário detectada.")
    finally:
        # O fechamento das conexões será gerenciado pelo script principal 'run_consumer.py'
        print("Finalizando o loop do consumidor...")