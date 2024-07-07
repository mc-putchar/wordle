# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logic.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: astavrop <astavrop@student.42berlin.de>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/07 15:27:44 by astavrop          #+#    #+#              #
#    Updated: 2024/07/07 17:07:46 by astavrop         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections import Counter
import sys

STATUS_CORRECT = "correct"
STATUS_INCOMPLETE = "incomplete"
STATUS_LOSER = "loser"
STATUS_MISS = "missing"
R_CORRECT = "correct"
R_PRESENT = "present"
R_ABSENT = "absent"


def check_word(attempt: str, secret: str):
    counts = dict(Counter(secret))
    result = []
    print(f"Secret\t:\t{secret}")
    print(f"User  \t:\t{attempt}")
    print()
    # LOOP 1
    for i in range(len(attempt)):
        if attempt[i] == secret[i]:
            result.append(R_CORRECT)
            counts[attempt[i]] -= 1
        else:
            result.append(R_ABSENT)
    print(f"Result: {result}\nCounts: {counts}")
    # LOOP 2
    for i in range(len(attempt)):
        if (attempt[i] in secret
            and counts[attempt[i]] > 0
            and result[i] == R_ABSENT):
            result[i] = R_PRESENT
            counts[attempt[i]] -= 1
    print("After LOOP 2")
    print(f"Result: {result}\nCounts: {counts}")
    print(enumaret(result))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        secret = sys.argv[1]
    else:
        secret = "hello"
    check_word(input("word? "), secret)
