from fastapi import FastAPI, Depends
from uuid import UUID
from entities import Answer
from model import SurveyAnswers
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/surveys", status_code=201)
async def create_survey(instance_name: str, db: Session = Depends(get_db)):
    answer = Answer()
    answer.content = "testcontent"
    answer.id = "testid2"
    db.add(answer)
    db.commit()
    db.flush()
    return {
        "message": "created",
        "instance_name": answer.content
    }


@app.get("/surveys/{survey_id}/results")
async def get_survey_results(survey_id: UUID):
    """Retrieve the survey and its results"""
    return {"id": survey_id}


@app.get("/surveys/{survey_id}")
async def get_survey(survey_id: UUID):
    return {"id": survey_id}


@app.post("/surveys/{survey_id}/answers", status_code=201)
async def complete_the_survey(survey_id: UUID, survey_answers: SurveyAnswers):
    score = 0.55
    return {
        "id": survey_id,
        "score": score,
        "request body": survey_answers
    }