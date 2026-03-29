import os  # O 'os' deve ser importado sozinho aqui
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

# Importações do seu projeto (mantenha como estava)
from controladores import roteador_produtos
from banco_dados import inicializar_banco, obter_engine

# --- CONFIGURAÇÃO INICIAL ---
app = FastAPI()

# Inicializa o banco de dados
inicializar_banco(obter_engine())

# Garante que as pastas existam
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/img", exist_ok=True)

# --- SEGURANÇA ---
security = HTTPBasic()
ADMIN_USER = "admin"
ADMIN_PASS = "dasdores123"

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

# 1. Rota Raiz: Redireciona direto para a vitrine da loja
@app.get("/")
async def raiz():
    return RedirectResponse(url="/static/loja.html")

# 2. Rota Admin Protegida
@app.get("/admin")
async def pagina_admin(username: str = Depends(verificar_autenticacao)):
    return FileResponse("static/index.html")

# 3. Inclui as rotas da API de produtos
app.include_router(roteador_produtos, prefix="/api/produtos")

# 4. Monta a pasta static (DEVE SER A ÚLTIMA LINHA DE CONFIGURAÇÃO)
app.mount("/static", StaticFiles(directory="static"), name="static")