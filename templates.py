from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@templates_router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
