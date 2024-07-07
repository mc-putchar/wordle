# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    wordle.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mcutura <mcutura@student.42berlin.de>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/06 01:06:12 by astavrop          #+#    #+#              #
#    Updated: 2024/07/07 06:16:43 by mcutura          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from datetime import date
import json
from os.path import isfile
from typing import Dict, List, Literal
import os

from fastapi import FastAPI
from pydantic import BaseModel, model_validator
from starlette.responses import FileResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func, select

from .database import session, Word, get_todays_word, set_todays_word, fill_db
from starlette.responses import FileResponse

app = FastAPI()


STATUS_CORRECT = "correct"
STATUS_INCOMPLETE = "incomplete"
STATUS_LOSER = "loser"
R_CORRECT = "correct"
R_PRESENT = "present"
R_ABSENT = "absent"
WORDS_FN = "words.txt"


class AttemptRequest(BaseModel):
    token: str
    attempt: str

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AttemptResponse(BaseModel):
    current_attempt: int
    status: Literal[STATUS_LOSER, STATUS_INCOMPLETE, STATUS_CORRECT]
    result: Dict[int, Literal[R_ABSENT, R_PRESENT, R_CORRECT]]


TODAYS_WORD = "abcde"


database = {}


@app.on_event("shutdown")
def close_db():
    session.close()


@app.on_event("startup")
def clone_words():
    with open(WORDS_FN, "r") as file:
        fill_db([word.replace("\n", "") for word in file.readlines()])


@app.get("/")
def index():
    return FileResponse("frontend/index.html")
@app.get("/style.css")
def style():
    return FileResponse("frontend/style.css")
@app.get("/wordle.js")
def script():
    return FileResponse("frontend/wordle.js")
@app.get("/favicon.ico")
def favicon():
    return FileResponse("frontend/favicon.ico")
@app.get("/wallpaper.jpg")
def wallpaper():
    return FileResponse("frontend/wallpaper.jpg")


@app.post("/word/")
def check_word(request: AttemptRequest):
    if request.token not in database.keys():
        database[request.token] = 1
    else:
        database[request.token] += 1

    # User exceeded number of attempts
    if database[request.token] > 5:
        return AttemptResponse(
            current_attempt=database[request.token], status=STATUS_LOSER, result={}
        )

    today = date.today()
    if session.query(Word).filter_by(day=today).count() < 1:
        correct_word: Word = set_todays_word(
            session.query(Word)
            .filter_by(is_assigned=False)
            .order_by(func.random())
            .first()
            .word
        )
    else:
        correct_word: Word = get_todays_word()
    print(correct_word.word)
    result = {}
    status: str = STATUS_LOSER
    mistakes = 0

    if request.attempt == correct_word.word:
        result = {i: R_CORRECT for i in range(len(request.attempt))}
        status = STATUS_CORRECT
    else:
        for index, letter in enumerate(request.attempt):
            if letter == correct_word.word[index]:
                result[index] = R_CORRECT
            elif letter in correct_word.word:
                if request.attempt.count(letter) == 1:
                    result[index] = R_PRESENT
                else:
                    result[index] = R_ABSENT
                mistakes += 1
            else:
                result[index] = R_ABSENT
                mistakes += 1

        if mistakes > 0 and status != STATUS_INCOMPLETE:
            status = STATUS_INCOMPLETE

    return AttemptResponse(
        current_attempt=database[request.token], status=status, result=result
    )
