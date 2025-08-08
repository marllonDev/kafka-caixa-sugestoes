from flask import Flask, request, jsonify
from . import producer  # Importa o nosso módulo producer
from . import config    # Importa o nosso módulo de configuração

# Aqui criamos a instância principal da nossa aplicação Flask.
# Mais tarde, nosso script 'run_api.py' irá importar esta variável 'app'.
app: Flask = Flask(__name__)

# --- Definição do Endpoint da API ---
@app.route('/sugestao', methods=['POST'])
def rota_enviar_sugestao():
    """
    Recebe uma sugestão em formato JSON via POST, valida os dados
    e delega o envio para o módulo do produtor Kafka.
    """
    # Pega os dados JSON enviados no corpo da requisição POST.
    dados_sugestao= request.get_json(force=True)

    # Validação simples para garantir que recebemos um JSON válido e com a chave 'sugestao'.
    if not dados_sugestao or 'sugestao' not in dados_sugestao:
        return jsonify({"status": "erro", "mensagem": "JSON inválido. 'sugestao' é um campo obrigatório."}), 400

    # Em vez de lidar com o Kafka diretamente, nós simplesmente chamamos a função
    # 'send_message' do nosso módulo 'producer', passando o tópico (que vem
    # do nosso config) e a mensagem.
    sucesso: bool = producer.send_message(topic=config.KAFKA_TOPIC, message=dados_sugestao)

    # Verificamos o resultado da função de envio.
    if sucesso:
        return jsonify({"status": "sucesso", "mensagem": "Sugestão recebida e enviada para processamento!"})
    else:
        # Se o produtor não conseguiu enviar, retornamos um erro de serviço indisponível.
        return jsonify({"status": "erro", "mensagem": "Serviço de sugestões indisponível no momento."}), 503

# No futuro, se quisermos criar o endpoint GET /sugestoes,
# nós o adicionaríamos aqui neste mesmo arquivo.