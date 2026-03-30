import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager

# Importações do seu projeto
from controladores import roteador_produtos
from banco_dados import inicializar_banco

# --- STARTUP EVENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco no Supabase
    inicializar_banco()
    yield

# ADICIONADO: redirect_slashes=False para evitar erros de barra final
app = FastAPI(lifespan=lifespan, redirect_slashes=False)

# Pastas de suporte
os.makedirs("static/uploads", exist_ok=True)

# --- SEGURANÇA ---
security = HTTPBasic()
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "dasdores123")

def verificar_autenticacao(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correto = secrets.compare_digest(credentials.username, ADMIN_USER)
    senha_correta = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (usuario_correto and senha_correta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- ROTAS ---

@app.get("/")
async def raiz():
    # Redireciona para a vitrine da Dasdores Móveis
    return RedirectResponse(url="/static/loja.html")

@app.get("/admin")
async def pagina_admin(username: str = Depends(verificar_autenticacao)):
    return FileResponse("static/index.html")

# Ajustado para bater com o seu controladores.py
app.include_router(roteador_produtos, prefix="/api/produtos")

# Montagem de arquivos estáticos (sempre por último)
app.mount("/static", StaticFiles(directory="static"), name="static")