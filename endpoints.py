from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import utils
from database import engine, Base, SessionLocal
from entities import Survey, SurveyResult
from model import SurveyAnswersRequest, SurveyResponse, SurveyResultResponse
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


@app.get("/surveys/{survey_id}/results", response_model=List[SurveyResultResponse])
async def get_survey_results(survey_id: UUID, db: Session = Depends(get_db)):
    survey = utils.get_survey(db, str(survey_id))
    return survey.results


@app.get("/surveys/{survey_id}", response_model=SurveyResponse)
async def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    survey = utils.get_survey(db, str(survey_id))
    return survey


@app.post("/surveys/{survey_id}/answers", status_code=201)
async def complete_the_survey(survey_id: UUID,
                              survey_answers: List[SurveyAnswersRequest],
                              nickname: str = Query(None, min_length=2, max_length=20),
                              db: Session = Depends(get_db)):
    survey = utils.get_survey(db, str(survey_id))
    correct_answers = 0
    survey_length = len(survey.questions)
    for question in survey.questions:
        relevant_answer_id = utils.get_relevant_answer_from_request(survey_answers, question.id)
        if relevant_answer_id is not None:
            if question.get_correct_answer().id == relevant_answer_id:
                correct_answers += 1
    survey_result = SurveyResult()
    survey_result.id = str(uuid4())
    survey_result.nickname = nickname
    survey_result.score = correct_answers / survey_length
    survey.results.append(survey_result)
    db.add(survey)
    db.commit()
    db.flush()
    return {
        "score": correct_answers,
        "question_count": survey_length
    }
