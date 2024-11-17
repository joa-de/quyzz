# Description: This file contains the function that generates 3 random wrong options plus the correct answer.
# Denis Joassin 2024

import random


def get_random_options(correct_answer, vocabulary, word_type=None):
    """
    Get random options for multiple choice, with support for word type matching.

    Args:
        correct_answer: The correct translation
        vocabulary: The complete vocabulary dictionary
        word_type: The type of word to match (for level 3)
    """
    options = [correct_answer]
    vocab_items = list(vocabulary.items())

    if word_type:
        # Filter vocabulary items to only include words of the same type
        same_type_items = [
            item
            for item in vocab_items
            if item[1]["word_type"] == word_type
            and item[1]["translation"] != correct_answer
        ]

        # If we don't have enough words of the same type, fall back to random words
        if len(same_type_items) < 3:
            different_items = [
                item for item in vocab_items if item[1]["translation"] != correct_answer
            ]
            while len(options) < 4:
                random_item = random.choice(different_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
        else:
            # Add three random words of the same type
            while len(options) < 4:
                random_item = random.choice(same_type_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
    else:
        # Original behavior for levels 1 and 2
        different_items = [
            item for item in vocab_items if item[1]["translation"] != correct_answer
        ]
        while len(options) < 4:
            random_item = random.choice(different_items)
            if random_item[1]["translation"] not in options:
                options.append(random_item[1]["translation"])

    # Shuffle the options
    random.shuffle(options)
    return options
