from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@templates_router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@templates_router.get("/survey/{survey_id}/results", response_class=HTMLResponse)
async def get_results_page(survey_id: UUID, request: Request):
    return templates.TemplateResponse("survey_results.html", {"request": request, "survey_id": survey_id})
