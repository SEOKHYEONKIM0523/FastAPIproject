from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.dbfactory import db_startup
from app.routes.board import board_router
from app.routes.gallery import gallery_router
from app.routes.member import member_router


# 서버 시작 시 DB 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_startup()


app = FastAPI(lifespan=lifespan)

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
app.mount('/static',StaticFiles(directory='views/static'),name='static')


# 외부 route 파일 불러오기
app.include_router(member_router)
app.include_router(board_router, prefix='/board')
app.include_router(gallery_router, prefix='/gallery')


@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',reload=True)