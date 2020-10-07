from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import utils
from database import engine, Base, SessionLocal
from entities import Survey
from model import SurveyAnswersRequest, SurveyResponse
from utils import generate_random_questions, is_answer_correct

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/surveys", status_code=201, response_model=SurveyResponse)
async def create_survey(instance_name: str, question_count: int = 2, db: Session = Depends(get_db)):
    survey = Survey()
    survey.id = str(uuid4())
    survey.instance_name = instance_name
    survey.questions = generate_random_questions(db, instance_name, question_count)
    db.add(survey)
    db.commit()
    db.flush()

    return {
        "id": survey.id,
        "instance_name": survey.instance_name,
        "questions": survey.questions
    }


@app.get("/surveys/{survey_id}/results")
async def get_survey_results(survey_id: UUID):
    """Retrieve the survey and its results"""
    return {"id": survey_id}


@app.get("/surveys/{survey_id}", response_model=SurveyResponse)
async def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    survey = utils.get_survey(db, str(survey_id))
    return survey


@app.post("/surveys/{survey_id}/answers", status_code=201)
async def complete_the_survey(survey_id: UUID, survey_answers: List[SurveyAnswersRequest],
                              db: Session = Depends(get_db)):
    survey = utils.get_survey(db, str(survey_id))
    score = 0
    survey_length = len(survey.questions)
    for answer in survey_answers:
        if is_answer_correct(db, answer.answer_id):
            score += 1
    return {
        "score": score,
        "question_count": survey_length
    }
