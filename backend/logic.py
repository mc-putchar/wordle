# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logic.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: astavrop <astavrop@student.42berlin.de>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/07 15:27:44 by astavrop          #+#    #+#              #
#    Updated: 2024/07/07 15:27:45 by astavrop         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections import Counter


def check_word(attempt: str):
    letters = set(attempt)
    counts = dict(Counter(list(attempt)))
    print(counts)


if __name__ == "__main__":
    check_word(input("word? "))
