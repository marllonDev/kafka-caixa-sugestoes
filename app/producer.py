import json
from kafka import KafkaProducer
from . import config  # Importa as nossas configurações centralizadas

# --- Variável Global para o Produtor ---
# Vamos criar uma única instância do produtor que pode ser reutilizada
# em toda a aplicação. Isso é mais eficiente do que criar uma nova a cada mensagem.
producer = None

# --- Função de Inicialização ---
def initialize_producer() -> None:
    """
    Inicializa a conexão com o Kafka e cria a instância do produtor.
    Esta função será chamada uma vez quando a nossa API iniciar.
    """
    # A palavra-chave 'global' nos permite modificar a variável 'producer'
    # que foi declarada fora desta função.
    global producer
    
    try:
        # Criamos a instância do Produtor, mas agora lendo as configurações
        # do nosso arquivo config.py, que importamos acima.
        producer = KafkaProducer(
            bootstrap_servers=config.KAFKA_SERVER,
            # O serializador continua o mesmo: converte nosso dicionário para JSON em bytes.
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ Produtor Kafka inicializado com sucesso!")
    except Exception as e:
        # Se a conexão falhar, informamos o erro e a variável 'producer'
        # continuará como 'None'.
        print(f"❌ Erro ao inicializar o produtor Kafka: {e}")
        producer = None

# --- Função para Enviar Mensagens ---
def send_message(topic, message):
    """
    Envia uma mensagem para um tópico específico do Kafka.

    Args:
        topic (str): O nome do tópico de destino.
        message (dict): A mensagem a ser enviada (em formato de dicionário).
    
    Returns:
        bool: True se a mensagem foi enviada para o buffer, False em caso de erro.
    """
    # Verificamos primeiro se a nossa instância do produtor foi inicializada com sucesso.
    if not producer:
        print("🚨 Produtor Kafka não está disponível.")
        return False
    
    try:
        # Usamos a instância global 'producer' para enviar a mensagem.
        print(f"📨 Enviando mensagem para o tópico '{topic}': {message}")
        producer.send(topic, value=message)
        # Força o envio de mensagens pendentes. É uma boa prática para garantir
        # que mensagens importantes não fiquem muito tempo no buffer.
        producer.flush()
        print("👍 Mensagem enviada com sucesso!")
        return True
    except Exception as e:
        print(f"🔥 Erro ao enviar mensagem: {e}")
        return False