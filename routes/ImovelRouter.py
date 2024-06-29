import datetime
from io import BytesIO
import os
from fastapi import (APIRouter, Depends, File, Form, HTTPException, Path, Request, UploadFile, status,)
from fastapi.templating import Jinja2Templates
from models.Imovel import Imovel
from models.Usuario import Usuario
from repositories.ImoveisRepo import ImoveisRepo
from util.imagem import transformar_em_quadrada
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado
from PIL import Image

router = APIRouter(prefix="/imovel")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_index(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    imoveis = ImoveisRepo.obter_todos()
    return templates.TemplateResponse("imovel/index.html", {"request": request, "usuario": usuario, "imoveis": imoveis, "now":datetime.datetime.now().timestamp()},)

@router.get("/inserir")
async def get_inserir(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return templates.TemplateResponse("imovel/inserir.html", {"request": request, "usuario": usuario},)

@router.post("/inserir")
async def post_inserir(nome: str = Form(...), preco: str = Form(...), descricao: str = Form(...), categoria: str = Form(...), destaque: bool = Form(...), arquivoImagem: UploadFile = File(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    categorias = {
        "1": 'Aluguel',
        "2": 'Venda',
    }

    categoria_input = ""

    if categoria not in categorias:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        categoria_input = categoria
    
    imovel = Imovel(nome=nome, preco=preco, descricao=descricao, categoria=categoria_input, destaque=destaque)

    print(imovel)

    # Inserir o imóvel no banco de dados
    print(ImoveisRepo.inserir(imovel))

    # Agora o id do imóvel deve estar definido
    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/imoveis/{imovel.id:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/imovel", "imovel inserido com sucesso!")
    return response

@router.get("/excluir/{id_imovel:int}")
async def get_excluir(request: Request, id_imovel: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    imovel = ImoveisRepo.obter_por_id(id_imovel)
    return templates.TemplateResponse("imovel/excluir.html", {"request": request, "usuario": usuario, "imovel": imovel},
)

@router.post("/excluir/{id_imovel:int}")
async def post_excluir(id_imovel: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # ImoveisRepo.excluir(id_imovel)
    ImoveisRepo().excluir(id_imovel)

    caminho_imagem = f"static/img/imoveis/{id_imovel:04d}.jpg"
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)

    response = redirecionar_com_mensagem("/imovel", "Imovel excluído com sucesso!")
    return response

@router.get("/alterar/{id_imovel:int}")
async def get_alterar(request: Request, id_imovel: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    imovel = ImoveisRepo.obter_por_id(id_imovel)
    return templates.TemplateResponse("imovel/alterar.html", {"request": request, "usuario": usuario, "imovel": imovel},)

@router.post("/alterar/{id_imovel:int}")
async def post_alterar(id_imovel: int = Path(), nome: str = Form(...), preco: str = Form(...), descricao: str = Form(...), categoria: str = Form(...), destaque: bool = Form(...), arquivoImagem: UploadFile = File(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    ImoveisRepo.alterar(Imovel(id_imovel, nome, preco, descricao, categoria, destaque))

    try:
        os.remove(f"static/img/imoveis/{id_imovel:04d}.jpg")
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")

    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/imoveis/{id_imovel:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/imovel", "imovel alterado com sucesso!")
    return response