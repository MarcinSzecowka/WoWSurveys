import time
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import usecases
import utils
from entities import Instance, ShortId
from utils import get_db

templates_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@templates_router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    instances = utils.get_instances(db)
    return templates.TemplateResponse("index.html", {"request": request, "instances": instances})


@templates_router.get("/survey/{survey_id}/results", response_class=HTMLResponse)
async def get_results_page(survey_id: UUID, request: Request, db: Session = Depends(get_db)):
    survey = usecases.get_survey(survey_id, db)
    if survey is None:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("survey_results.html", {"request": request, "survey": survey})


@templates_router.get("/survey/{public_survey_id}", response_class=HTMLResponse)
async def get_survey(public_survey_id: UUID, request: Request, db: Session = Depends(get_db)):
    survey = usecases.get_survey_by_public_id(public_survey_id, db)
    if survey is None:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("survey_form.html", {"request": request, "survey": survey})


@templates_router.get("/result", response_class=HTMLResponse)
async def get_user_result(request: Request):
    return templates.TemplateResponse("survey_user_result.html", {"request": request})


@templates_router.get("/{short_id}", response_class=HTMLResponse)
async def redirect(short_id: str, db: Session = Depends(get_db)):
    if usecases.is_path_a_short_id(short_id, db):
        new_path = db.query(ShortId).filter(ShortId.short_id == short_id).first()
        return RedirectResponse("/survey/" + new_path.public_id)
    else:
        return RedirectResponse("/")
