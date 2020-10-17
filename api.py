from typing import List
from uuid import UUID

from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session

import usecases
import utils
from database import engine, Base, SessionLocal
from model import SurveyAnswersRequest, SurveyResponse, SurveyResultResponse

data_file_name = "data.json"

Base.metadata.create_all(bind=engine)

api_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


utils.initialize_database(data_file_name, next(get_db()))


@api_router.post("/api/surveys", status_code=201, response_model=SurveyResponse)
async def create_survey(instance_name: str, question_count: int = 2, db: Session = Depends(get_db)):
    return usecases.create_survey(instance_name, question_count, db)


@api_router.get("/api/surveys/{survey_id}/results", response_model=List[SurveyResultResponse])
async def get_survey_results(survey_id: UUID, db: Session = Depends(get_db)):
    return usecases.get_survey_results(survey_id, db)


@api_router.get("/api/surveys/{survey_id}", response_model=SurveyResponse)
async def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    return usecases.get_survey(survey_id, db)


@api_router.post("/api/surveys/{survey_id}/answers", status_code=201)
async def complete_the_survey(survey_id: UUID,
                              survey_answers: List[SurveyAnswersRequest],
                              nickname: str = Query(None, min_length=2, max_length=20),
                              db: Session = Depends(get_db)):
    correct_answers, survey_length = usecases.complete_the_survey(survey_id, survey_answers, nickname, db)
    return {
        "score": correct_answers,
        "question_count": survey_length
    }
