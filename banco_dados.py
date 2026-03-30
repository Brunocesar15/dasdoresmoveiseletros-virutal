from sqlmodel import create_engine, SQLModel
from supabase import create_client, Client
import os


URL_BANCO_DADOS = "postgresql+psycopg2://postgres:dasdoresadm@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
# 2. Configurações da API do Supabase (Para o Upload de Fotos)
SUPABASE_URL = "https://ndgfnachjiveazzwdccg.supabase.co"
# Cole aqui a sua chave ANON (aquela longa que começa com eyJhbGci...)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5kZ2ZuYWNoaml2ZWF6endkY2NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4ODcyNzksImV4cCI6MjA5MDQ2MzI3OX0.LmFxvG6NaU8LGa6IMXB_ErHYFrEVDf5UNSv-w6AzeYc" 

# --- CRIAÇÃO DOS OBJETOS ---

# O motor para o SQLModel
engine = create_engine(URL_BANCO_DADOS, echo=False)

# O cliente para o Storage (É ISSO QUE O CONTROLADORES.PY ESTÁ BUSCANDO)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNÇÕES DE APOIO ---

def obter_engine():
    return engine

def inicializar_banco():
    """Cria as tabelas no Supabase se elas não existirem"""
    try:
        SQLModel.metadata.create_all(engine)
        print("✅ Tabelas sincronizadas no Supabase com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao sincronizar tabelas: {e}")
