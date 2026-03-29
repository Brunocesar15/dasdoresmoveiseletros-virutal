from sqlmodel import SQLModel, create_engine

# Padronizando para o nome que usamos no README e nos comandos Git
URL_BANCO_DADOS = 'sqlite:///database.db'

# O check_same_thread=False é importante para o FastAPI não dar erro com SQLite
engine = create_engine(URL_BANCO_DADOS, connect_args={"check_same_thread": False})

def obter_engine():
    return engine

def inicializar_banco():
    SQLModel.metadata.create_all(engine)