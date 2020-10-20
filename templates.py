from uuid import UUID

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from usecases import get_survey
from utils import get_db

templates_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@templates_router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@templates_router.get("/survey/{survey_id}/results", response_class=HTMLResponse)
async def get_results_page(survey_id: UUID, request: Request, db: Session = Depends(get_db)):
    survey = get_survey(survey_id, db)
    return templates.TemplateResponse("survey_results.html", {"request": request, "survey": survey})
