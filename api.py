import datetime
import secrets
import os
from typing import List
from uuid import UUID

from fastapi import Depends, Query, APIRouter, HTTPException
from sqlalchemy.orm import Session

import usecases
import utils
from database import engine, Base, SessionLocal
from model import SurveyAnswersRequest, SurveyResponse, SurveyResultResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

questions_data_name = "questions_data.json"
instances_data_name = "instances_data.json"

Base.metadata.create_all(bind=engine)

api_router = APIRouter()

security = HTTPBasic()

utils.initialize_database(questions_data_name, instances_data_name, next(utils.get_db()))


@api_router.post("/api/surveys", status_code=201, response_model=SurveyResponse)
async def create_survey(instance_name: str, question_count: int = 2, db: Session = Depends(utils.get_db)):
    return usecases.create_survey(instance_name, question_count, db)


@api_router.get("/api/surveys/{survey_id}/results", response_model=List[SurveyResultResponse])
async def get_survey_results(survey_id: UUID, db: Session = Depends(utils.get_db)):
    return usecases.get_survey_results(survey_id, db)


@api_router.get("/api/surveys/{survey_public_id}", response_model=SurveyResponse)
async def get_survey(survey_public_id: UUID, db: Session = Depends(utils.get_db)):
    return usecases.get_survey_by_public_id(survey_public_id, db)


@api_router.post("/api/surveys/{survey_public_id}/answers", status_code=201)
async def complete_the_survey(survey_public_id: UUID,
                              survey_answers: List[SurveyAnswersRequest],
                              client_id: str = Query(None, min_length=32, max_length=32),
                              nickname: str = Query(None, min_length=2, max_length=20),
                              db: Session = Depends(utils.get_db)):
    if client_id is None:
        raise HTTPException(status_code=400)
    if not usecases.is_client_eligible_to_complete_the_survey(str(survey_public_id), client_id, db):
        raise HTTPException(status_code=429)
    score = usecases.complete_the_survey(survey_public_id, survey_answers, client_id, nickname, db)
    return {
        "score": score,
    }


@api_router.delete("/api/surveys")
async def delete_expired_surveys(credentials: HTTPBasicCredentials = Depends(security),
                                 db: Session = Depends(utils.get_db)):
    login = os.environ.get("WOWSURVEYS_LOGIN")
    password = os.environ.get("WOWSURVEYS_PASSWORD")
    correct_username = secrets.compare_digest(credentials.username, login)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return usecases.delete_expired_surveys(db)
