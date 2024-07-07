# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    database.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: astavrop <astavrop@student.42berlin.de>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/06 20:21:17 by astavrop          #+#    #+#              #
#    Updated: 2024/07/07 22:08:25 by astavrop         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import date
from sqlalchemy import Column, String, Date, Boolean, Integer, create_engine, except_
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLA_DB_URL = "sqlite:///./wordle.db"

engine = create_engine(
        SQLA_DB_URL, connect_args={"check_same_thread": False}
        )
Base = declarative_base()

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True, nullable=False)
    day = Column(Date, nullable=True)
    is_assigned = Column(Boolean, nullable=False)

    def __init__(self, word, is_assigned, day=None) -> None:
        self.word = word
        self.is_assigned = is_assigned
        self.day = day


class Player(Base):
    __tablename__ = "players"

    # UUID recieved from frontend
    id = Column(String, primary_key=True)
    attempt_n = Column(Integer, default=0, nullable=False)
    is_finished = Column(Boolean, default=False)
    # 1 - playing, 2 - won, 3 - lost
    state = Column(Integer, default=1)
    prev_tries = Column(String, default="")

    def __init__(self, id, attempt_n=0) -> None:
        self.id = id
        self.attempt_n = attempt_n


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def get_todays_word():
    today = date.today()
    return session.query(Word).filter_by(day=today).first()

def set_todays_word(word: str):
    today = date.today()
    if session.query(Word).filter_by(day=today).first():
        raise Exception("Today's word is already set")
    new_word = session.query(Word).filter_by(word=word).first()
    if new_word:
        new_word.day = today
        new_word.is_assigned = True
    else:
        new_word = Word(word=word, is_assigned=True, day=today)
        session.add(new_word)

    session.commit()
    return new_word

def fill_db(words: list[str]):
    if not words:
        raise Exception("No words to put into database")
    print(f"Loading {len(words)} words")
    for word in words:
        if session.query(Word).filter_by(word=word.strip()).count() < 1:
            print(f":: {word}             ", end="\r")
            new_word = Word(word=word.strip(), is_assigned=False)
            session.add(new_word)
    print(" "*10)
    session.commit()
