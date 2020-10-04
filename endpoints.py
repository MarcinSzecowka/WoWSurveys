from fastapi import FastAPI, Depends
from uuid import UUID, uuid4
from utils import generate_random_questions
from entities import Answer, Question, Survey
from model import SurveyAnswers, QuestionResponse, SurveyResponse
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from typing import List

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
    survey.id = uuid4().hex
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


@app.get("/surveys/{survey_id}", response_model=QuestionResponse)
async def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    question = Question()
    question.content = "testquestion"
    question.id = "testid19"
    db.add(question)
    db.commit()
    db.flush()
    return {
        "content": question.content,
    }


@app.post("/surveys/{survey_id}/answers", status_code=201)
async def complete_the_survey(survey_id: UUID, survey_answers: SurveyAnswers):
    score = 0.55
    return {
        "id": survey_id,
        "score": score,
        "request body": survey_answers
    }
