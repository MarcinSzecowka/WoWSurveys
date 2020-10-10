import json
import random
from typing import List

from sqlalchemy.orm import Session

from entities import Question, Answer, Survey
from model import SurveyAnswersRequest


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


def convert_answers_to_entities(answers):
    answers_list = []
    for answer in answers:
        answer_entity = Answer()
        answer_entity.id = answer["id"]
        answer_entity.content = answer["content"]
        answer_entity.is_correct = answer["is_correct"]
        answers_list.append(answer_entity)
    return answers_list


def initialize_database(data_file_name: str, db: Session):
    question_ids = get_questions_ids_from_database(db)
    questions = load_questions_from_file(data_file_name)
    question_count = 0
    for question in questions:
        if question["id"] not in question_ids:
            question_entity = Question()
            question_entity.id = question["id"]
            question_entity.content = question["content"]
            question_entity.instance_name = question["instance_name"]
            question_entity.answers = convert_answers_to_entities(question["answers"])
            db.add(question_entity)
            question_count += 1
    db.commit()
    db.flush()
    if question_count != 0:
        print(f"Loaded:{question_count} questions")
    else:
        print("Didn't load any new questions")


def load_questions_from_file(data_file_name: str):
    with open(data_file_name, encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_questions_ids_from_database(db: Session):
    questions = db.query(Question).all()
    question_ids = []
    for question in questions:
        question_ids.append(question.id)
    return question_ids
