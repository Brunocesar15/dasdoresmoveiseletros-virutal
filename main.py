import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager # Para um startup mais limpo

# Importações do seu projeto
from controladores import roteador_produtos
from banco_dados import inicializar_banco

# --- STARTUP EVENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco (Sincroniza tabelas no Supabase)
    inicializar_banco()
    yield

app = FastAPI(lifespan=lifespan)

# Mantemos as pastas apenas para arquivos que já vão no seu GIT (CSS, JS, Imagens fixas)
os.makedirs("static/uploads", exist_ok=True)

# --- SEGURANÇA (ADMIN_USER e PASS deveriam vir do .env) ---
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
    return RedirectResponse(url="/static/loja.html")

@app.get("/admin")
async def pagina_admin(username: str = Depends(verificar_autenticacao)):
    # Certifique-se de que static/index.html é a sua página de gerenciar produtos
    return FileResponse("static/index.html")

# Prefixo ajustado para evitar /api/produtos/produtos
app.include_router(roteador_produtos, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")