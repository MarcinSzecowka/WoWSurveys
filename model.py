from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class SurveyAnswer(BaseModel):
    question_id: UUID
    answer_id: UUID


class SurveyAnswers(BaseModel):
    answers: list


class SurveyResponse(BaseModel):
    id: str
    instance_name: str
    questions: List


class QuestionResponse(BaseModel):
    id: str
    content: str
    answers: List


class AnswerResponse(BaseModel):
    id: str
    content: str
    is_correct: bool
