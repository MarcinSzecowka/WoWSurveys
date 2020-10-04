from sqlalchemy import Column, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base

survey_questions_association_table = Table("survey_questions", Base.metadata,
                                           Column("survey_id", String, ForeignKey("surveys.id")),
                                           Column("question_id", String, ForeignKey("questions.id"))
                                           )

question_answers_association_table = Table("question_answers", Base.metadata,
                                           Column("question_id", String, ForeignKey("questions.id")),
                                           Column("answer_id", String, ForeignKey("answers.id"))
                                           )


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(String, primary_key=True, index=True)
    instance_name = Column(String)
    questions = relationship("Question", secondary=survey_questions_association_table)


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    instance_name = Column(String, index=True)
    answers = relationship("Answer", secondary=question_answers_association_table)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    is_correct = Column(Boolean)
