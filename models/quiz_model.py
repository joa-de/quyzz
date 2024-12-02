# Description: This file contains the function that generates 3 random wrong options plus the correct answer.
# Denis Joassin 2024

import random


class QuizModel:
    def __init__(self):
        pass

    def get_random_options(
        correct_answer, correct_answer_id, vocabulary, word_type=None
    ):
        """
        Get random options for multiple choice, with support for word type matching.

        Args:
            correct_answer: The correct translation
            vocabulary: The complete vocabulary dictionary
            word_type: The type of word to match (for level 3)
        """
        options = [correct_answer]
        options_id = [correct_answer_id]
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
                    item
                    for item in vocab_items
                    if item[1]["translation"] != correct_answer
                ]
                while len(options) < 4:
                    random_item = random.choice(different_items)
                    if random_item[1]["translation"] not in options:
                        options.append(random_item[1]["translation"])
                        options_id.append(random_item[0])
            else:
                # Add three random words of the same type
                while len(options) < 4:
                    random_item = random.choice(same_type_items)
                    if random_item[1]["translation"] not in options:
                        options.append(random_item[1]["translation"])
                        options_id.append(random_item[0])
        else:
            # Original behavior for levels 1 and 2
            different_items = [
                item for item in vocab_items if item[1]["translation"] != correct_answer
            ]
            while len(options) < 4:
                random_item = random.choice(different_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
                    options_id.append(random_item[0])

        # Shuffle the options
        combined = list(zip(options, options_id))
        random.shuffle(combined)
        options, options_id = zip(*combined)

        return options, options_id
