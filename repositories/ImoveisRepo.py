import sqlite3
from typing import List, Optional
from models.Imovel import Imovel
from sql.ImovelSql import *
from util.bancodedados import criar_conexao

class ImoveisRepo:
    @classmethod
    def criar_tabela(cls) -> bool:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error as e:
            print(e)
            return False
    
    @classmethod
    def inserir(cls, imovel: Imovel) -> Optional[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR_IMOVEL, (imovel.nome, imovel.preco, imovel.descricao, imovel.categoria, imovel.destaque))
                if cursor.rowcount > 0:
                    imovel.id = cursor.lastrowid
                    return imovel
        except sqlite3.Error as e:
            print(e)
            return None
        
    @classmethod
    def obter_destaques(cls, destaques) -> List[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                imoveis = cursor.execute(SQL_OBTER_DESTAQUES, (destaques)).fetchall()
                return [Imovel(*p) for p in imoveis]
        except sqlite3.Error as e:
            print(e)
            return None
    
    @classmethod
    def obter_todos(cls) -> List[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                imoveis = cursor.execute(SQL_OBTER_TODOS).fetchall()
                return [Imovel(*p) for p in imoveis]
        except sqlite3.Error as e:
            print(e)
            return None
        
    @classmethod
    def obter_imoveis(cls, categoria) -> List[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                imoveis = cursor.execute(SQL_OBTER_CATEGORIA, (categoria)).fetchall()
                return [Imovel(*p) for p in imoveis]
        except sqlite3.Error as e:
            print(e)
            return None
        
    @classmethod
    def pesquisar(cls, nome) -> List[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                imoveis = cursor.execute(SQL_PESQUISAR, (nome)).fetchall()
                return [Imovel(*p) for p in imoveis]
        except sqlite3.Error as e:
            print(e)
            return None
        
    @classmethod
    def alterar(cls, imovel: Imovel) -> Optional[Imovel]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR,(imovel.nome, imovel.preco, imovel.descricao, imovel.categoria, imovel.destaque ,imovel.id))
            if cursor.rowcount > 0:
                return imovel
        except sqlite3.Error as e:
            print(e)
            return None
    
    classmethod
    def excluir(cls, id_imovel: int) -> bool or False: # type: ignore
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_imovel,))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as e:
            print(e)
            return None
        
    @classmethod
    def obter_por_id(cls, id_imovel: int) -> Imovel or None: # type: ignore
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                imovel = cursor.execute(SQL_OBTER_POR_ID, (id_imovel,)).fetchone()
                return Imovel(*imovel)
        except sqlite3.Error as e:
            print(e)
            return None