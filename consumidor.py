import json
import time
from kafka import KafkaConsumer

# Nome do tópico que vamos "ouvir"
TOPIC_NAME = 'sugestoes-topic'
# ID do grupo de consumidores para nossa "equipe de operários"
GROUP_ID = 'grupo-sugestoes-arquivistas'
# Endereço do nosso servidor Kafka (agora acessível do seu PC)
BOOTSTRAP_SERVERS = 'localhost:9092'

print("➡️  Iniciando Consumidor Kafka...")
print(f"   Tópico: {TOPIC_NAME}")
print(f"   Grupo de Consumidores: {GROUP_ID}")

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

if not consumer:
    print("🚨 Não foi possível conectar ao Kafka. Encerrando o consumidor.")
else:
    print("\n🎧 Ouvindo o tópico em busca de novas sugestões...")
    try:
        # Este loop fica 'travado', esperando por novas mensagens.
        for message in consumer:
            sugestao = message.value
            
            # Ação principal: Imprimir a mensagem recebida!
            print("\n----------------------------------------------------")
            print(f"📬 Nova sugestão recebida!")
            print(f"   - Partição: {message.partition}")
            print(f"   - Offset: {message.offset}")
            print(f"   - Conteúdo: {sugestao}")
            print("----------------------------------------------------")

    except KeyboardInterrupt:
        print("\n\n🔌 Desligando o consumidor...")
    finally:
        consumer.close()