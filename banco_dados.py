from sqlmodel import create_engine, SQLModel
import os

# 1. Ajuste na URL: Adicionamos 'ql' no postgres e o parâmetro de SSL
URL_BANCO_DADOS = "postgresql://postgres:dasdoresadm@db.ndgfnachjiveazzwdccg.supabase.co:5432/postgres?sslmode=require"

# 2. Criamos o engine (o motor de conexão)
# O echo=True ajuda a ver no terminal o que o banco está fazendo (bom para testes)
engine = create_engine(URL_BANCO_DADOS, echo=False)

def obter_engine():
    return engine

def inicializar_banco():
    # Isso cria as tabelas automaticamente no Supabase se elas não existirem
    try:
        SQLModel.metadata.create_all(engine)
        print("✅ Tabelas sincronizadas no Supabase com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao sincronizar tabelas: {e}")