import json
import random
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import SessionLocal
from entities import Question, Answer, Survey, SurveyResult, Instance
from model import SurveyAnswersRequest


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_random_questions(db: Session, instance_name: str, category: str, question_count: int):
    all_questions = db.query(Question)\
        .filter(or_(Question.instance_name == instance_name, Question.category == category))\
        .all()
    if question_count > len(all_questions):
        return all_questions
    return random.sample(all_questions, question_count)


def get_survey(db: Session, survey_id: str) -> SurveyResult:
    return db.query(Survey).filter(Survey.id == survey_id).first()


def get_survey_by_public_id(db: Session, survey_public_id: str) -> SurveyResult:
    return db.query(Survey).filter(Survey.public_id == survey_public_id).first()


def get_instances(db: Session) -> Instance:
    return db.query(Instance).all()


def is_answer_correct(db: Session, answer_id: str):
    return db.query(Answer).filter(answer_id == Answer.id, Answer.is_correct).count() == 1


def get_relevant_answer_from_request(survey_answers: List[SurveyAnswersRequest], question_id: str) -> str:
    for answer in survey_answers:
        if answer.question_id == question_id:
            return answer.answer_id
    return None


def convert_answers_to_entities(answers):
    answers_list = []
    for answer in answers:
        answer_entity = Answer()
        answer_entity.id = answer["id"]
        answer_entity.content = answer["content"]
        answer_entity.is_correct = answer["is_correct"]
        answers_list.append(answer_entity)
    return answers_list


def initialize_database(questions_data_name: str, instances_data_name: str, db: Session):
    initialize_questions(questions_data_name, db)
    initialize_instances(instances_data_name, db)


def initialize_instances(instances_data_name, db):
    instances = load_data_from_file(instances_data_name)
    for instance in instances:
        instance_entity = Instance()
        instance_entity.name = instance["name"]
        instance_entity.category = instance["category"]
        db.add(instance_entity)
    try:
        db.commit()
        db.flush()
    except IntegrityError:
        print("Integrity error handled")



def initialize_questions(questions_data_name, db):
    question_ids = get_questions_ids_from_database(db)
    questions = load_data_from_file(questions_data_name)
    question_count = 0
    for question in questions:
        if question["id"] not in question_ids:
            question_entity = Question()
            question_entity.id = question["id"]
            question_entity.content = question["content"]
            question_entity.instance_name = question.get("instance_name")
            question_entity.category = question["category"]
            question_entity.answers = convert_answers_to_entities(question["answers"])
            db.add(question_entity)
            question_count += 1
    db.commit()
    db.flush()
    if question_count != 0:
        print(f"Loaded:{question_count} questions")
    else:
        print("Didn't load any new questions")


def load_data_from_file(data_file_name: str):
    with open(data_file_name, encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_questions_ids_from_database(db: Session):
    questions = db.query(Question).all()
    question_ids = []
    for question in questions:
        question_ids.append(question.id)
    return question_ids
