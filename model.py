from pydantic import BaseModel
from uuid import UUID


class SurveyAnswer(BaseModel):
    question_id: UUID
    answer_id: UUID


class SurveyAnswers(BaseModel):
    answers: list
