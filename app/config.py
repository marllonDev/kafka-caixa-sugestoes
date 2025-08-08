import os
from dotenv import load_dotenv

# Esta função carrega as variáveis de ambiente do arquivo .env
# localizado na raiz do projeto.
load_dotenv()

# --- Configurações do Kafka ---
# Buscamos cada variável do ambiente usando os.getenv()
# e a armazenamos em uma constante Python para fácil acesso.
KAFKA_SERVER: str | None = os.getenv('KAFKA_SERVER')
KAFKA_TOPIC: str | None = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP: str | None = os.getenv('KAFKA_CONSUMER_GROUP')

# --- Configurações do Banco de Dados PostgreSQL ---
DB_HOST: str | None = os.getenv('DB_HOST')
DB_PORT: str | None = os.getenv('DB_PORT')
DB_NAME: str | None = os.getenv('DB_NAME')
DB_USER: str | None = os.getenv('DB_USER')
DB_PASSWORD: str | None = os.getenv('DB_PASSWORD')