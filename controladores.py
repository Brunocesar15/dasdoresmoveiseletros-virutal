from fastapi import APIRouter, status, HTTPException, File, UploadFile, Form
from modelos import ProdutoModel
from servicos import ProdutoServico
# Importe a conexão do seu arquivo de banco
from banco_dados import supabase 
import uuid

roteador_produtos = APIRouter()
produto_servico = ProdutoServico()

async def fazer_upload_supabase(imagem: UploadFile):
    """Função auxiliar para enviar ao Storage e retornar a URL"""
    extensao = imagem.filename.split(".")[-1]
    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    caminho_storage = f"fotos/{nome_arquivo}"
    
    conteudo = await imagem.read()
    
    # Faz o upload para o bucket 'produtos'
    supabase.storage.from_("produtos").upload(
        path=caminho_storage,
        file=conteudo,
        file_options={"content-type": f"image/{extensao}"}
    )
    
    # Retorna a URL Pública
    return supabase.storage.from_("produtos").get_public_url(caminho_storage)

@roteador_produtos.post("", status_code=status.HTTP_201_CREATED)
async def adicionar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade_estoque: int = Form(...),
    categoria: str = Form(...),
    imagem: UploadFile = File(...),
    destaque: bool = Form(False) 
):
    # Envia para a Nuvem em vez de salvar localmente
    url_publica = await fazer_upload_supabase(imagem)

    # Criar modelo com a URL da internet
    novo_produto = ProdutoModel(
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
        categoria=categoria,
        imagem_url=url_publica, # <-- Link fixo e eterno
        destaque=destaque
    )
    return produto_servico.salvar_produto(novo_produto)

@roteador_produtos.put("/{id}")
async def editar_produto(
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade_estoque: int = Form(...),
    categoria: str = Form(...),
    imagem: UploadFile = File(None), 
    destaque: bool = Form(False)
):
    dados_atualizados = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade_estoque": quantidade_estoque,
        "categoria": categoria,
        "destaque": destaque 
    }

    # Se enviou nova imagem, sobe para o Supabase
    if imagem and imagem.filename:
        url_publica = await fazer_upload_supabase(imagem)
        dados_atualizados["imagem_url"] = url_publica

    produto = produto_servico.atualizar_produto(id, dados_atualizados)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

# Mantemos as rotas GET e DELETE como estavam...
@roteador_produtos.get("/{id}")
def obter_produto_por_id(id: int):
    return produto_servico.obter_produto_por_id(id=id)

@roteador_produtos.get("/")
def listar_produtos(nome: str | None = None, preco: float | None = None, categoria: str | None = None):
    return produto_servico.listar_produtos(nome=nome, preco=preco, categoria=categoria)

@roteador_produtos.delete("/{id}")
def excluir_produto(id: int):
    sucesso = produto_servico.excluir_produto(id=id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": "Produto removido com sucesso"}