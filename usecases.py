import datetime
from typing import List, Tuple
from uuid import uuid4, UUID

from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session
import time
import utils
from entities import Survey, SurveyResult, Instance, ShortId
from model import SurveyAnswersRequest
from utils import generate_random_questions


def create_survey(instance_name: str, question_count: int, db: Session) -> Survey:
    instance = db.query(Instance).filter(Instance.name == instance_name).first()
    survey = Survey()
    survey.id = str(uuid4())
    survey.public_id = str(uuid4())
    survey.instance = instance
    survey.created_at = datetime.datetime.utcnow()
    survey.questions = generate_random_questions(db, instance_name, instance.category, question_count)
    short_id = utils.generate_random_short_id(db)
    timestamp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    short_id_entity = ShortId()
    survey.short_id = short_id_entity
    short_id_entity.short_id = short_id
    short_id_entity.expiration_date_utc = timestamp
    short_id_entity.public_id = survey.public_id
    db.add(survey)
    db.commit()
    db.flush()
    return survey


def get_survey(survey_id: UUID, db: Session) -> Survey:
    return utils.get_survey(db, str(survey_id))


def get_survey_by_public_id(survey_public_id: UUID, db: Session) -> Survey:
    return utils.get_survey_by_public_id(db, str(survey_public_id))


def get_survey_results(survey_id: UUID, db: Session) -> SurveyResult:
    return utils.get_survey(db, str(survey_id)).results


def complete_the_survey(survey_public_id: UUID,
                        survey_answers: List[SurveyAnswersRequest],
                        client_id: str,
                        nickname: str,
                        db: Session) -> float:
    survey = utils.get_survey_by_public_id(db, str(survey_public_id))
    correct_answers = 0
    survey_length = len(survey.questions)
    for question in survey.questions:
        relevant_answer_id = utils.get_relevant_answer_from_request(survey_answers, question.id)
        if relevant_answer_id is not None:
            if question.get_correct_answer().id == relevant_answer_id:
                correct_answers += 1
    survey_result = SurveyResult()
    survey_result.id = str(uuid4())
    survey_result.client_id = client_id
    survey_result.created_at_timestamp = datetime.datetime.utcnow()
    survey_result.nickname = nickname
    survey_result.score = correct_answers / survey_length
    survey.results.append(survey_result)
    db.add(survey)
    db.commit()
    db.flush()
    return survey_result.score


def is_path_a_short_id(any_path: str, db: Session):
    return db.query(ShortId).filter(ShortId.short_id == any_path).count() == 1


def is_client_eligible_to_complete_the_survey(survey_public_id: str,
                                              client_id: str,
                                              db: Session):
    ts_minus_an_hour = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    clients_last_response = db.query(SurveyResult).\
        join(Survey).\
        filter(and_(Survey.public_id == survey_public_id,
                    SurveyResult.client_id == client_id)).\
        order_by(SurveyResult.created_at_timestamp.desc())\
        .first()
    if clients_last_response is None:
        return True
    return clients_last_response.created_at_timestamp < ts_minus_an_hour


def delete_surveys(surveys, timestamp, db: Session):
    deleted_surveys_count = 0
    for survey in surveys:
        if survey.created_at < timestamp:
            db.delete(survey)
            deleted_surveys_count += 1
    return deleted_surveys_count


def delete_expired_surveys(db: Session):
    deleted_surveys_count = 0

    ts_minus_one_day = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    all_dungeon_surveys = db.query(Survey).join(Instance).filter(Instance.category == "DUNGEON").all()
    deleted_surveys_count += delete_surveys(all_dungeon_surveys, ts_minus_one_day, db)

    ts_minus_one_week = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
    all_raid_surveys = db.query(Survey).join(Instance).filter(Instance.category == "RAID").all()
    deleted_surveys_count += delete_surveys(all_raid_surveys, ts_minus_one_week, db)

    db.commit()
    db.flush()
    return deleted_surveys_count
