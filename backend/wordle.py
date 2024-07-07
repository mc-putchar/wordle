# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    wordle.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mcutura <mcutura@student.42berlin.de>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/06 01:06:12 by astavrop          #+#    #+#              #
#    Updated: 2024/07/07 17:21:43 by mcutura          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from datetime import date
import json
from os.path import isfile
from typing import Dict, List, Literal
import os
from collections import Counter

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
STATUS_MISS = "missing"
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
    status: Literal[STATUS_MISS, STATUS_LOSER, STATUS_INCOMPLETE, STATUS_CORRECT]
    result: Dict[int, Literal[R_ABSENT, R_PRESENT, R_CORRECT]]


TODAYS_WORD = "abcde"


database = {}


@app.on_event("shutdown")
def close_db():
    session.close()


@app.on_event("startup")
def clone_words():
    if not os.path.exists("wordle.db"):
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
    if session.query(Word).filter_by(word=request.attempt).count() < 1:
        return AttemptResponse(current_attempt=0, status=STATUS_MISS, result={})

    if request.token not in database.keys():
        database[request.token] = 1
    else:
        database[request.token] += 1

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
    status: str = STATUS_LOSER

    if request.attempt == correct_word.word:
        result = {i: R_CORRECT for i in range(len(request.attempt))}
        status = STATUS_CORRECT
    else:
        counts = dict(Counter(correct_word.word))
        result = []
        for i in range(len(request.attempt)):
            if request.attempt[i] == correct_word.word[i]:
                result.append(R_CORRECT)
                counts[request.attempt[i]] -= 1
            else:
                result.append(R_ABSENT)
        for i in range(len(request.attempt)):
            if (
                request.attempt[i] in correct_word.word
                and counts[request.attempt[i]] > 0
                and result[i] == R_ABSENT
            ):
                result[i] = R_PRESENT
                counts[request.attempt[i]] -= 1
        result = {i: result[i] for i in range(len(result))}

    # User exceeded number of attempts
    if database[request.token] > 5:
        status = STATUS_LOSER

    return AttemptResponse(
        current_attempt=database[request.token], status=status, result=result
    )
