# Importamos as peças que precisamos de dentro do nosso pacote 'app'
from app.routes import app
from app.producer import initialize_producer

# A "mágica" acontece aqui.
# Este é o ponto de entrada principal para rodar nossa API.
# A construção 'if __name__ == "__main__":' garante que o código
# só será executado quando rodarmos o script diretamente.
if __name__ == '__main__':

    # PASSO 1: Primeiro, inicializamos nossa conexão com o Kafka.
    # É importante que a conexão seja estabelecida ANTES de a API
    # começar a aceitar requisições dos usuários.
    print("Iniciando o serviço da API de Sugestões...")
    initialize_producer()

    # PASSO 2: Depois que o produtor está pronto, iniciamos o servidor Flask.
    # A variável 'app' que importamos de 'routes' contém todas as nossas
    # definições de endpoints (como o /sugestao).
    app.run(host='0.0.0.0', port=5000, debug=True)