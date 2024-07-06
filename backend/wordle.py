# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    wordle.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: astavrop <astavrop@student.42berlin.de>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/06 01:06:12 by astavrop          #+#    #+#              #
#    Updated: 2024/07/06 01:07:42 by astavrop         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import json
from typing import Dict, List, Literal

from fastapi import FastAPI
from pydantic import BaseModel, model_validator

app = FastAPI()


STATUS_CORRECT = "correct"
STATUS_INCOMPLETE = "incomplete"
STATUS_LOSER = "loser"
R_CORRECT = "correct"
R_PRESENT = "present"
R_ABSENT = "absent"


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


@app.get("/")
def read_root():
    return {"Hello": "Wordle"}


@app.post("/word/")
def check_word(request: AttemptRequest):
    if request.token not in database.keys():
        database[request.token] = 1
    else:
        database[request.token] += 1

    # User exceeded number of attempts
    if database[request.token] >= 5:
        return AttemptResponse(
            current_attempt=database[request.token], status=STATUS_LOSER, result={}
        )

    correct_word = str(TODAYS_WORD)
    result = {}
    status: str = STATUS_LOSER
    mistakes = 0

    if request.attempt == correct_word:
        result = {i: R_CORRECT for i in range(len(request.attempt))}
        status = STATUS_CORRECT
    else:
        for index, letter in enumerate(request.attempt):
            if letter == correct_word[index]:
                result[index] = R_CORRECT
            elif letter in correct_word:
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
