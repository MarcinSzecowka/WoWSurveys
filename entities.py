from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    survey_id = Column(String, ForeignKey("surveys.id"))
    answers = relationship("Answer", back_populates="question")
    survey = relationship("Survey", back_populates="questions")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    question_id = Column(String, ForeignKey("questions.id"))
    is_correct = Column(Boolean)
    question = relationship("Question", back_populates="answers")


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(String, primary_key=True, index=True)
    instance_name = Column(String)
    questions = relationship("Question", back_populates="survey")
