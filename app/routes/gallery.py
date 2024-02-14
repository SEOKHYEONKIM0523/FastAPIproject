from math import ceil

from fastapi import APIRouter, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import status
from app.schemas.board import NewBoard
from app.services.board import BoardService

gallery_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')
gallery_router.mount('/static',StaticFiles(directory='views/static'),name='static')

@gallery_router.get('/list/{cpg}', response_class=HTMLResponse)
def list(req: Request, cpg: int):
    # stpg = int((cpg -1) / 10 ) * 10 + 1   #페이지네이션 시작값
    # galist, cnt = BoardService.select_gallery(cpg)
    # allpage = ceil(cnt / 25) # 총 페이지 수
    return templates.TemplateResponse('gallery/list.html',
    {'request': req, 'gallist': None, 'cpg':cpg, 'stpg':1, 'allpage': 1, 'baseurl':'/gallery/list/'})

@gallery_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def find(req: Request, ftype: str, fkey: str, cpg: int):
    stpg = int((cpg -1) / 10 ) * 10 + 1
    # gallist, cnt = BoardService.find_select_gallery(ftype,'%' + fkey + '%', cpg)
    # allpage = ceil(cnt / 25)
    return templates.TemplateResponse('gallery/list.html',
                                      {'request': req, 'galllist': None, 'cpg':cpg, 'stpg':stpg, 'allpage': 1,
                                       'baseurl': f'/gallery/list/{ftype}/{fkey}/'})


@gallery_router.get('/write', response_class=HTMLResponse)
def write(req: Request):
    return templates.TemplateResponse('gallery/write.html', {'request': req})


@gallery_router.post('/write')
async def writeok(title: str = Form(),userid: str = Form(),contents: str = Form(), attach: UploadFile = File() ):

    res_url = '/gallery/list/1'



    # print(title, userid, contents)
    # print(attach.filename, attach.content_type, attach.size)

    UPLOAD_DIR = r'C:\Java\nginx-1.25.3\html\cdn'
    fname = UPLOAD_DIR + r'\\20240214' + attach.filename

    # 비동기 처리를 위해 함수에 await 지시자 추가
    # 이럴 경우 함수 정의 부분에 async라는 지시자 추가 필요
    content = await attach.read() #업로드한 파일의 내용을 비동기로 모두 읽어옴
    with open(fname, 'wb') as f:
        f.write(content)

    # if BoardService.check_captcha(bdto): #captcha 체크가 true라면
    #     result = BoardService.insert_gallery(bdto)
    #     res_url = '/error'
    #     if result.rowcount > 0: res_url = '/gallery/list/1'

    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@gallery_router.get('/view/{gno}', response_class=HTMLResponse)
def view(req: Request, gno: str):
    # bd = BoardService.selectone_gallery(gno)[0]
    # BoardService.update_count_gallery(gno)
    return templates.TemplateResponse('gallery/view.html', {'request': req, 'bd': None})
