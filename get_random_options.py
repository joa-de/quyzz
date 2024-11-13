# Description: This file contains the function that generates 3 random wrong options plus the correct answer.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

import random


def get_random_options(correct_answer, vocabulary):
    """Generate 3 random wrong options plus the correct answer."""
    options = [correct_answer]
    possible_answers = [
        d["translation"]
        for d in vocabulary.values()
        if d["translation"] != correct_answer
    ]
    options.extend(random.sample(possible_answers, 3))
    random.shuffle(options)
    return options
