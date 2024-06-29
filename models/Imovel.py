from dataclasses import dataclass
from typing import Optional

@dataclass
class Imovel:
    id: Optional[int] = None
    nome: Optional[str] = None
    preco: Optional[int] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    destaque: Optional[bool] = False