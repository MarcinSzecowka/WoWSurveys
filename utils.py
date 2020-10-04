import random
from uuid import uuid4

from sqlalchemy.orm import Session

from entities import Question, Answer
from typing import List

from model import QuestionResponse, AnswerResponse


# def convert_questions_to_response(questions: List[Question]):
#     question_responses = []
#     for question in questions:
#         question_response = QuestionResponse()
#         question_response.id = question.id
#         question_response.content = question.content
#         question_response.answers = convert_answers_to_response(question.answers)
#         question_responses.append(question_response)
#
#     return question_responses
#
#
# def convert_answers_to_response(answers: List[Answer]):
#     answer_responses = []
#     for answer in answers:
#         answer_response = AnswerResponse()
#         answer_response.id = answer.id
#         answer_response.content = answer.content
#         answer_response.is_correct = answer.is_correct
#         answer_responses.append(answer_response)
#
#     return answer_responses


def generate_random_questions(db: Session, instance_name: str, question_count: int):
    all_questions = db.query(Question).filter(Question.instance_name == instance_name).all()
    if question_count > len(all_questions):
        return all_questions
    return random.sample(all_questions, question_count)
