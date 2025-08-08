from flask import Flask, request, jsonify, json
from . import producer  # Importa o nosso módulo producer
from . import config    # Importa o nosso módulo de configuração
from . import database  # Importa o nosso módulo de banco de dados


# Aqui criamos a instância principal da nossa aplicação Flask.
# Mais tarde, nosso script 'run_api.py' irá importar esta variável 'app'.
app: Flask = Flask(__name__)

# --- Definição do Endpoint POST da API ---
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


# --- Endpoint GET ---
@app.route('/sugestoes', methods=['GET'])
def rota_get_sugestoes():
    """
    Busca todas as sugestões no banco de dados e as retorna como JSON.
    """
    print("Recebida requisição para buscar todas as sugestões.")
    
    # Simplesmente chamamos a função do nosso especialista em banco de dados.
    sugestoes= database.get_all_sugestoes()
    
    # O psycopg2 retorna objetos de data/hora que não são diretamente
    # serializáveis para JSON. A função json.dumps com o parâmetro 'default=str'
    # resolve isso, convertendo esses objetos em strings.
    # O Flask.jsonify não tem essa opção, então fazemos a conversão em duas etapas.
    response_data: str = json.dumps(sugestoes, default=str)
    
    # Criamos uma resposta Flask a partir do JSON formatado.
    return app.response_class(
        response=response_data,
        status=200,
        mimetype='application/json'
    )