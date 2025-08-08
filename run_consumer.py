# Importamos as funções que precisamos de dentro do nosso pacote 'app'
from app.consumer import initialize_consumer, start_consuming
from app.database import initialize_database, close_database

# O ponto de entrada principal para rodar nosso consumidor.
if __name__ == '__main__':
    print("▶️  Iniciando o serviço do Consumidor de Sugestões...")
    
    # PASSO 1: Inicializa as conexões com os serviços externos.
    # Primeiro com o banco de dados, depois com o Kafka.
    db_ok: bool= initialize_database()
     # Adicionamos este print para ver o resultado da conexão com o banco
    print(f"--> Status da conexão com o Banco de Dados (db_ok): {db_ok}")

    consumer_ok: bool = initialize_consumer()
    # Adicionamos este print para ver o resultado da conexão com o Kafka
    print(f"--> Status da conexão com o Kafka (consumer_ok): {consumer_ok}")

    # PASSO 2: Só inicia o processo se ambas as conexões foram bem-sucedidas.
    if db_ok and consumer_ok:
        try:
            # Chama a função que contém o loop infinito de 'escuta' do Kafka.
            start_consuming()
        finally:
            # O bloco 'finally' é uma garantia. Ele SEMPRE será executado
            # ao sair do bloco 'try', não importa o motivo (seja por um erro
            # ou por você pressionar Ctrl+C no terminal).
            # É o local perfeito para garantir que recursos importantes, como
            # a conexão com o banco, sejam sempre liberados.
            print("\nEncerrando o serviço do consumidor.")
            close_database()
    else:
        print("🚨 Não foi possível inicializar os serviços necessários. Encerrando.")