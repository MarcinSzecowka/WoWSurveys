import random
from uuid import uuid4

from sqlalchemy.orm import Session

from entities import Question, Answer, Survey
from typing import List

from model import AnswerResponse, SurveyAnswersRequest


def generate_random_questions(db: Session, instance_name: str, question_count: int):
    all_questions = db.query(Question).filter(Question.instance_name == instance_name).all()
    if question_count > len(all_questions):
        return all_questions
    return random.sample(all_questions, question_count)


def get_survey(db: Session, survey_id: str):
    return db.query(Survey).filter(Survey.id == survey_id).first()


def is_answer_correct(db: Session, answer_id: str):
    return db.query(Answer).filter(answer_id == Answer.id, Answer.is_correct).count() == 1


def get_relevant_answer_from_request(survey_answers: List[SurveyAnswersRequest], question_id: str) -> str:
    for answer in survey_answers:
        if answer.question_id == question_id:
            return answer.answer_id
    return None
