from sqlalchemy import Column, String, ForeignKey, Boolean, Table, Float
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
    public_id = Column(String, index=True)
    questions = relationship("Question", secondary=survey_questions_association_table)
    results = relationship("SurveyResult")
    instance_name = Column(String, ForeignKey("instances.name"))
    instance = relationship("Instance")


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    instance_name = Column(String, index=True)
    category = Column(String)
    answers = relationship("Answer", secondary=question_answers_association_table)

    def get_correct_answer(self):
        for answer in self.answers:
            if answer.is_correct:
                return answer
        return None


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    is_correct = Column(Boolean)


class SurveyResult(Base):
    __tablename__ = "survey_results"
    id = Column(String, primary_key=True, index=True)
    nickname = Column(String)
    score = Column(Float)
    survey = Column(String, ForeignKey('surveys.id'))


class Instance(Base):
    __tablename__ = "instances"
    name = Column(String, primary_key=True, index=True)
    category = Column(String)
