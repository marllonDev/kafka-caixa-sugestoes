import psycopg2
from . import config  # Importa as nossas configurações centralizadas

# --- Variável Global para a Conexão ---
# Assim como fizemos com o produtor, criaremos uma única conexão com o banco
# que será compartilhada, o que é muito mais eficiente.
db_connection = None

# --- Função de Inicialização ---
def initialize_database() -> None:
    """
    Inicializa a conexão com o banco de dados PostgreSQL.
    Esta função será chamada uma vez quando o consumidor iniciar.
    """
    global db_connection
    
    try:
        # Usamos os dados do nosso arquivo config para estabelecer a conexão.
        db_connection = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        print("✅ Conexão com o PostgreSQL inicializada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar a conexão com o PostgreSQL: {e}")
        db_connection = None

# --- Função para Salvar a Sugestão ---
def save_sugestao(sugestao_data) -> bool:
    """
    Recebe um dicionário com os dados da sugestão e o salva no banco.

    Args:
        sugestao_data (dict): Dicionário contendo a sugestão.
    
    Returns:
        bool: True se a operação foi bem-sucedida, False em caso de erro.
    """
    # Verifica se a conexão com o banco foi estabelecida.
    if not db_connection:
        print("🚨 Conexão com o banco de dados não está disponível.")
        return False

    # Pega os dados do dicionário, definindo 'Anônimo' como padrão se o autor não existir.
    autor = sugestao_data.get('autor', 'Anônimo')
    sugestao_texto = sugestao_data.get('sugestao')

    # Só tenta inserir se o texto da sugestão não for vazio.
    if not sugestao_texto:
        print("⚠️ Sugestão vazia recebida. Nenhum dado foi salvo.")
        return False

    try:
        # Cria um 'cursor' para executar os comandos SQL.
        # O 'with' garante que o cursor será fechado automaticamente.
        with db_connection.cursor() as cursor:
            sql = "INSERT INTO sugestoes (autor, sugestao) VALUES (%s, %s);"
            cursor.execute(sql, (autor, sugestao_texto))
        
        # Confirma a transação para salvar os dados permanentemente.
        db_connection.commit()
        print(f"💾 Sugestão de '{autor}' salva no banco de dados com sucesso!")
        return True
    except Exception as e:
        print(f"🔥 Erro ao salvar no banco de dados: {e}")
        # Se ocorrer um erro, reverte a transação para não deixar o banco
        # em um estado inconsistente.
        db_connection.rollback()
        return False

# --- Função para Fechar a Conexão ---
def close_database() -> None:
    """Fecha a conexão com o banco de dados, se ela estiver aberta."""
    if db_connection:
        db_connection.close()
        print("❌ Conexão com o PostgreSQL fechada.")