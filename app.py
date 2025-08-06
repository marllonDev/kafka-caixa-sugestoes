# Arquivo: app.py

import json
from flask import Flask, request, jsonify
from kafka import KafkaProducer

# --- 1. Inicialização e Configuração ---

# Cria a nossa aplicação Flask. O '__name__' é uma variável especial do Python
# que ajuda o Flask a saber onde encontrar outros arquivos, se precisarmos.
app = Flask(__name__)

# Configuração do nosso Produtor Kafka.
# Ele tentará se conectar ao Kafka assim que a aplicação iniciar.
try:
    # Criamos o objeto do Produtor.
    # - bootstrap_servers: Informa o endereço do nosso broker Kafka. Como nossa API
    #   está rodando localmente (fora do Docker), nos conectamos via 'localhost:9092',
    #   a porta que expusemos no docker-compose.
    # - value_serializer: O Kafka envia mensagens como bytes. Esta função lambda
    #   pega nosso dicionário Python (JSON), o converte para uma string e depois
    #   para o formato de bytes UTF-8, que é o que o Kafka espera.
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("✅ Produtor Kafka conectado com sucesso!")
    
except Exception as e:
    # Se a conexão com o Kafka falhar ao iniciar, o programa avisará e não continuará.
    # Isso é importante para não termos uma API rodando que não consegue fazer seu trabalho.
    print(f"❌ Erro ao conectar com o Kafka: {e}")
    producer = None

# --- 2. Definição do Endpoint da API ---

# Aqui definimos a nossa "rota" ou "endpoint".
# - '/sugestao': É o endereço (ex: http://localhost:5000/sugestao).
# - methods=['POST']: Especifica que este endpoint só aceita requisições do tipo POST.
@app.route('/sugestao', methods=['POST'])
def enviar_sugestao():
    """
    Recebe uma sugestão em formato JSON e a envia para o tópico Kafka.
    """
    # Primeiro, verificamos se o nosso produtor Kafka está conectado.
    if not producer:
        # Se não estiver, retornamos um erro 503 (Serviço Indisponível).
        return jsonify({"status": "erro", "mensagem": "Serviço de sugestões indisponível"}), 503

    # Pega os dados JSON enviados no corpo da requisição POST.
    # O 'force=True' ajuda a evitar erros se o cabeçalho 'Content-Type' não for 'application/json'.
    dados_sugestao = request.get_json(force=True)

    # Verificação simples para garantir que recebemos um JSON válido e com a chave 'sugestao'.
    if not dados_sugestao or 'sugestao' not in dados_sugestao:
        # Se os dados forem inválidos, retornamos um erro 400 (Bad Request).
        return jsonify({"status": "erro", "mensagem": "JSON inválido. 'sugestao' é um campo obrigatório."}), 400

    # O nome do tópico para onde enviaremos a mensagem.
    # É o mesmo que definimos em nossa arquitetura.
    topic_name = 'sugestoes-topic'

    try:
        # AQUI A MÁGICA ACONTECE!
        # Usamos o método 'send' do produtor para enviar a mensagem.
        # - 1º argumento: O nome do tópico.
        # - value: O conteúdo da mensagem (nosso dicionário/JSON).
        print(f"📨 Enviando sugestão para o tópico '{topic_name}': {dados_sugestao}")
        producer.send(topic_name, value=dados_sugestao)
        
        # O Kafka Producer funciona de forma assíncrona. As mensagens são colocadas
        # em um buffer e enviadas em background. 'flush()' força o envio
        # imediato de todas as mensagens pendentes no buffer.
        producer.flush()

        print("👍 Mensagem enviada com sucesso!")
        
        # Retornamos uma resposta de sucesso para quem chamou a API.
        return jsonify({"status": "sucesso", "mensagem": "Sugestão recebida e enviada para processamento!"})

    except Exception as e:
        # Se algo der errado durante o envio, capturamos o erro.
        print(f"🔥 Erro ao enviar mensagem para o Kafka: {e}")
        # E retornamos uma mensagem de erro genérica para o cliente.
        return jsonify({"status": "erro", "mensagem": "Ocorreu um erro interno ao processar a sugestão."}), 500

# --- 3. Execução da Aplicação ---

# Este bloco só é executado quando rodamos o script diretamente (python app.py).
# Ele não é executado se o arquivo for importado por outro.
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask.
    # - host='0.0.0.0': Faz o servidor ser acessível por qualquer IP da máquina, não só localhost.
    # - port=5000: Define a porta em que a API vai rodar.
    # - debug=True: Ativa o modo de depuração, que reinicia o servidor automaticamente
    #   a cada alteração no código e mostra erros detalhados no navegador. Ótimo para desenvolver.
    app.run(host='0.0.0.0', port=5000, debug=True)