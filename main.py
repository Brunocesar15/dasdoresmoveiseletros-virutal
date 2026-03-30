import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Importações do seu projeto
from controladores import roteador_produtos
from banco_dados import inicializar_banco

# --- STARTUP EVENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco no Supabase
    inicializar_banco()
    yield

# Removi o redirect_slashes=False para o FastAPI ser mais flexível
app = FastAPI(lifespan=lifespan)

# Pastas de suporte
os.makedirs("static/uploads", exist_ok=True)

# --- MIDDLEWARE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- ROTAS DA API (Sempre antes dos arquivos estáticos) ---

# Incluímos o roteador APENAS UMA VEZ
app.include_router(roteador_produtos, prefix="/api/produtos", tags=["Produtos"])

@app.get("/")
async def raiz():
    # Redireciona para a vitrine
    return RedirectResponse(url="/static/loja.html")

@app.get("/admin")
async def pagina_admin(username: str = Depends(verificar_autenticacao)):
    return FileResponse("static/index.html")

# --- ARQUIVOS ESTÁTICOS (Sempre por último) ---
app.mount("/static", StaticFiles(directory="static"), name="static")