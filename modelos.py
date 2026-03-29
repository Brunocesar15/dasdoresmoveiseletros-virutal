from sqlmodel import Field, SQLModel

class ProdutoModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int
    categoria: str
    material: str | None = None # Novo
    dimensoes: str | None = None # Novo
    imagem_url: str | None = None # Onde guardaremos o caminho da foto
    destaque: bool = Field(default=False) # VIP