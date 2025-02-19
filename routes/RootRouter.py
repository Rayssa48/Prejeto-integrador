from fastapi import APIRouter, Depends, Form, HTTPException, Path, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.ImoveisRepo import ImoveisRepo
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.mensagem import adicionar_cookie_mensagem, redirecionar_com_mensagem
from util.seguranca import adicionar_cookie_autenticacao, conferir_senha, excluir_cookie_autenticacao, gerar_token, obter_hash_senha, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    imoveis = ImoveisRepo.obter_destaques(destaques="1")
    return templates.TemplateResponse("root/index.html", {"request": request, "usuario": usuario, "imoveis": imoveis},)

@router.get("/avenda", response_class=HTMLResponse)
async def get_root(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    imoveis = ImoveisRepo.obter_imoveis("2")
    print(imoveis)
    return templates.TemplateResponse("root/avenda.html", {"request": request, "usuario": usuario, "imoveis": imoveis},)

@router.get("/alugueis", response_class=HTMLResponse)
async def get_root(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    imoveis = ImoveisRepo.obter_imoveis("1")
    print(imoveis)
    return templates.TemplateResponse("root/alugueis.html", {"request": request, "usuario": usuario, "imoveis": imoveis},)

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    return templates.TemplateResponse("root/login.html", {"request": request, "usuario": usuario},)

@router.post("/login", response_class=RedirectResponse)
async def post_login(email: str = Form(...), senha: str = Form(...), return_url: str = Query("/"),):
    hash_senha_bd = UsuarioRepo.obter_senha_por_email(email)
    if conferir_senha(senha, hash_senha_bd):
        token = gerar_token()
        UsuarioRepo.alterar_token_por_email(token, email)
        response = RedirectResponse(return_url, status.HTTP_302_FOUND)
        adicionar_cookie_autenticacao(response, token)
        adicionar_cookie_mensagem(response, "Login realizado com sucesso.")
    else:
        response = redirecionar_com_mensagem("/login", "Credenciais inválidas. Tente novamente.",)
    return response 

@router.get("/logout")
async def get_logout(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario:
        UsuarioRepo.alterar_token_por_email("", usuario.email)
        response = RedirectResponse("/", status.HTTP_302_FOUND)
        excluir_cookie_autenticacao(response)
        adicionar_cookie_mensagem(response, "Saída realizada com sucesso.")
    return response

@router.get("/imovel/{id_imovel:int}")
async def get_imoveis_descricao(request: Request, id_imovel: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    imovel = ImoveisRepo.obter_por_id(id_imovel)
    return templates.TemplateResponse("root/detalhes.html", {"request": request, "usuario": usuario, "imovel": imovel},)

@router.get("/arearestrita", response_class=HTMLResponse)
async def get_area_restrita(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return templates.TemplateResponse("root/arearestrita.html", {"request": request, "usuario": usuario},)

@router.post("/alterardados", response_class=HTMLResponse)
async def alterar_dados(
    nome: str = Form(...),
    email: str = Form(...),
    usuario: Usuario = Depends(obter_usuario_logado),
    ):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if usuario.id == 1:
        response = redirecionar_com_mensagem("/usuario", "Não é possível alterar dados do administrador padrão.",)
        return response
    
    UsuarioRepo.alterar(Usuario(id=usuario.id, nome=nome, email=email, admin=usuario.admin))

    response = redirecionar_com_mensagem("/arearestrita", "Dados alterados com sucesso.",)

    return response

@router.post("/alterarsenha", response_class=HTMLResponse)
async def alterar_senha(senha_atual: str = Form(...), nova_senha: str = Form(...), conf_nova_senha: str = Form(...), usuario: Usuario = Depends(obter_usuario_logado)):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    hash_senha_bd = UsuarioRepo.obter_senha_por_email(usuario.email)

    if conferir_senha(senha_atual, hash_senha_bd):
        if nova_senha == conf_nova_senha:
            hash_nova_senha = obter_hash_senha(nova_senha)
            UsuarioRepo.alterar_senha(Usuario(senha=hash_nova_senha,email=usuario.email))
            response = redirecionar_com_mensagem("/arearestrita", "Senha alterada com sucesso")
        else:
            response = redirecionar_com_mensagem("/arearestrita", "As senhas não coincidem!")
    else:
        response = redirecionar_com_mensagem("/arearestrita", "Informe a senha atual corretamente!")

    return response
