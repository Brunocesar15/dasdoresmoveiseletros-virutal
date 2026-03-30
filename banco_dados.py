import psycopg2
from psycopg2.extras import RealDictCursor

# Formato: postgres://postgres:[SUA_SENHA]@ndgfnachjiveazzwdccg.supabase.co:5432/postgres
DB_URL = "postgres://postgres:dasdoresadm@ndgfnachjiveazzwdccg.supabase.co:5432/postgres"

def get_connection():
    try:
        # O Supabase exige SSL para conexões externas por segurança
        conn = psycopg2.connect(DB_URL, sslmode='require')
        print("Conexão com o Supabase realizada com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Supabase: {e}")
        return None

# Teste rápido de conexão
if __name__ == "__main__":
    connection = get_connection()
    if connection:
        connection.close()