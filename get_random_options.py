# Description: This file contains the function that generates 3 random wrong options plus the correct answer.
# Denis Joassin 2024

import random


def get_random_options(correct_answer, correct_answer_id, vocabulary, word_type=None):
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
                item for item in vocab_items if item[1]["translation"] != correct_answer
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


def get_random_options_master(
    correct_answer, vocabulary, word_type=None, mastery_data=None
):
    """
    Get random options for multiple choice, with support for word type matching and difficulty adjustment.

    Args:
        correct_answer: The correct translation
        vocabulary: The complete vocabulary dictionary
        word_type: The type of word to match (for levels 3 and 4)
        mastery_data: Dictionary with performance data (for level 4)
    """
    options = [correct_answer]
    vocab_items = list(vocabulary.items())

    if word_type and mastery_data:
        # Filter vocabulary items by word type
        same_type_items = [
            item
            for item in vocab_items
            if item[1]["type"] == word_type and item[1]["translation"] != correct_answer
        ]

        # Sort by mastery: prioritize unplayed words, then difficult ones
        sorted_items = sorted(
            same_type_items,
            key=lambda item: (
                mastery_data[item[0]]["total_attempts"] == 0,  # Unplayed first
                mastery_data[item[0]]["correct_attempts"]
                / (mastery_data[item[0]]["total_attempts"] + 1),  # Difficulty ratio
            ),
        )

        # Pick top candidates
        for item in sorted_items:
            if len(options) >= 4:
                break
            if item[1]["translation"] not in options:
                options.append(item[1]["translation"])

        # Fallback to random options if not enough
        while len(options) < 4:
            random_item = random.choice(same_type_items)
            if random_item[1]["translation"] not in options:
                options.append(random_item[1]["translation"])
    else:
        # Original behavior for levels 1-3
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
