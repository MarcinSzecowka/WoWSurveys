from sqlalchemy import Column, String, ForeignKey, Boolean, Table, Float, TIMESTAMP
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
    public_id = Column(String, primary_key=True, index=True)
    questions = relationship("Question", secondary=survey_questions_association_table)
    results = relationship("SurveyResult")
    instance_name = Column(String, ForeignKey("instances.name"))
    instance = relationship("Instance")
    short_id = relationship("ShortId", uselist=False, back_populates="survey")


class ShortId(Base):
    __tablename__ = "short_ids"
    short_id = Column(String, primary_key=True)
    expiration_date_utc = Column(TIMESTAMP)
    public_id = Column(String, ForeignKey("surveys.public_id"))
    survey = relationship("Survey", back_populates="short_id")


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
    client_id = Column(String, index=True)
    created_at_timestamp = Column(TIMESTAMP)
    survey = Column(String, ForeignKey('surveys.id'))


class Instance(Base):
    __tablename__ = "instances"
    name = Column(String, primary_key=True, index=True)
    category = Column(String)
