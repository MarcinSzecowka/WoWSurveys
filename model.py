from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class SurveyAnswersRequest(BaseModel):
    question_id: str
    answer_id: str


class AnswerResponse(BaseModel):
    id: str
    content: str

    class Config:
        orm_mode = True


class QuestionResponse(BaseModel):
    id: str
    content: str
    answers: List[AnswerResponse]

    class Config:
        orm_mode = True


class SurveyResponse(BaseModel):
    id: str
    instance_name: str
    questions: List[QuestionResponse]

    class Config:
        orm_mode = True


class SurveyResultResponse(BaseModel):
    nickname: str
    score: float

    class Config:
        orm_mode = True
