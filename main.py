from fastapi import FastAPI # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
import uvicorn # type: ignore
from routes.RootRouter import router as rootRouter
from routes.UsuarioRouter import router as usuarioRouter
from util.seguranca import atualizar_cookie_autenticacao
from repositories.UsuarioRepo import UsuarioRepo
from repositories.ImoveisRepo import ImoveisRepo
from routes.ImovelRouter import router as imoveisRouter
from util.excecoes import configurar_paginas_de_erro

UsuarioRepo.criar_tabela()
UsuarioRepo.criar_administrador_padrao()
UsuarioRepo.criar_usuario_padrao()
ImoveisRepo.criar_tabela()

app = FastAPI()

app.middleware("http")(atualizar_cookie_autenticacao)
configurar_paginas_de_erro(app)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(rootRouter)
app.include_router(usuarioRouter)
app.include_router(imoveisRouter)

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000)

# host="192.168.100.76", reload=True