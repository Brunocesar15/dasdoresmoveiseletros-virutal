from sqlmodel import Session, select
from banco_dados import obter_engine
from modelos import ProdutoModel  # Este é o nome correto do seu modelo
from fastapi import status, HTTPException
from dtos import ProdutoDTO, AtualizarEstoqueDTO

class ProdutoServico:
    def __init__(self):
        self.engine = obter_engine()

    def obter_produto_por_id(self, id: int):
        with Session(self.engine) as sessao:
            consulta = select(ProdutoModel).where(ProdutoModel.id == id)
            return sessao.exec(consulta).one_or_none()
  
    def listar_produtos(self, nome: str | None = None, preco: float | None = None, categoria: str | None = None):
        with Session(self.engine) as sessao:
            consulta = select(ProdutoModel)
            if nome:
                consulta = consulta.where(ProdutoModel.nome.contains(nome)) # Busca aproximada
            if preco:
                consulta = consulta.where(ProdutoModel.preco <= preco)
            if categoria:
                consulta = consulta.where(ProdutoModel.categoria == categoria)
                
            return sessao.exec(consulta).all()
  
    def salvar_produto(self, produto: ProdutoModel):
        with Session(self.engine) as sessao:
            sessao.add(produto)
            sessao.commit()
            sessao.refresh(produto)
            return produto

    def atualizar_estoque(self, id: int, dados_estoque: AtualizarEstoqueDTO):
        with Session(self.engine) as sessao:
            produto = self.obter_produto_por_id(id)
            if not produto:
                raise ValueError("Produto não encontrado")
            
            nova_quantidade = produto.quantidade_estoque + dados_estoque.quantidade
            if nova_quantidade < 0:
                raise ValueError("Não é possível vender mais do que o estoque disponível")

            produto.quantidade_estoque = nova_quantidade
            sessao.commit()
            sessao.refresh(produto)
            return produto

    def excluir_produto(self, id: int):
        with Session(self.engine) as sessao:
            # Buscamos o produto diretamente na sessão atual
            consulta = select(ProdutoModel).where(ProdutoModel.id == id)
            produto = sessao.exec(consulta).one_or_none()
            
            if not produto:
                return False # Retorna Falso se não achar, para o controlador dar o erro 404
            
            sessao.delete(produto)
            sessao.commit()
            return True
    def atualizar_produto(self, id: int, dados: dict):
        with Session(self.engine) as sessao:
            consulta = select(ProdutoModel).where(ProdutoModel.id == id)
            produto = sessao.exec(consulta).one_or_none()
        
            if not produto:
                return None
            
            # ATENÇÃO: Tudo abaixo deve estar DENTRO do 'with Session'
            produto.nome = dados["nome"]
            produto.preco = dados["preco"]
            produto.categoria = dados["categoria"]
            produto.descricao = dados["descricao"]
            produto.quantidade_estoque = dados["quantidade_estoque"]
            
            # Nova linha para os Destaques da Dadores Móveis
            if "destaque" in dados:
                produto.destaque = dados["destaque"]
            
            # Só atualiza a imagem se ela foi enviada no dicionário
            if "imagem_url" in dados:
                produto.imagem_url = dados["imagem_url"]
            
            sessao.add(produto)
            sessao.commit()
            sessao.refresh(produto)
            return produto