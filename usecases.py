from typing import List, Tuple
from uuid import uuid4, UUID

from sqlalchemy.orm import Session

import utils
from entities import Survey, SurveyResult
from model import SurveyAnswersRequest
from utils import generate_random_questions


def create_survey(instance_name: str, question_count: int, db: Session) -> Survey:
    survey = Survey()
    survey.id = str(uuid4())
    survey.instance_name = instance_name
    survey.questions = generate_random_questions(db, instance_name, question_count)
    db.add(survey)
    db.commit()
    db.flush()
    return survey


def get_survey(survey_id: UUID, db: Session) -> Survey:
    return utils.get_survey(db, str(survey_id))


def get_survey_results(survey_id: UUID, db: Session) -> SurveyResult:
    return utils.get_survey(db, str(survey_id)).results


def complete_the_survey(survey_id: UUID,
                        survey_answers: List[SurveyAnswersRequest],
                        nickname: str,
                        db: Session) -> Tuple[int, int]:
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
    return correct_answers, survey_length