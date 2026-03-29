from pydantic import BaseModel

class ProdutoDTO(BaseModel):
    nome: str
    descricao: str 
    preco: float
    quantidade_estoque: int
    categoria: str
    material: str | None
    dimensoes: str | None

class AtualizarEstoqueDTO(BaseModel):
    quantidade: int