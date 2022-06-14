from guess_number.persist import persist_results, accumulate

import math
import structlog

log = structlog.get_logger()


def _next_guess(start, end, last_answer):
    """
    Sub-routine to handle generating the next guess
    from state in guess_number.
    """
    log.msg('generating guess', last_answer=last_answer, start=start, end=end)
    dictate = False

    # Log an unexpected erorr condition if end is smaller than start
    if end < start:
        log.msg('End has exceeded start',
                last_answer=last_answer, start=start, end=end)

    # If there is only one guess left then dictate the answer
    if (end - start) == 0:
        dictate = True
    if (end - start) <= 1:
        # Handle the edge case where math.floor is not sufficient to
        # find the pivot
        if last_answer == 'h':
            guess = start
        if last_answer == 'l':
            guess = end
    else:
        # Pivot the possibilities in the center point
        guess = math.floor(start + ((end - start)/2))
    return (dictate, guess)


def guess_number(start, end, correct_cb):
    """
    Guess a mystery secret number between start and end values.
    Check each concurrent guess against correct_cb callback function
    to determine if the current guess is too high or too low.
    """
    correct = False
    num_guesses = 0
    answer = 'l'
    while not correct:
        num_guesses += 1
        dictate, guess = _next_guess(start, end, answer)
        if dictate:
            return (guess, num_guesses)
        answer = correct_cb(guess)
        log.msg('Checking guess', start=start,
                end=end, guess=guess, answer=answer)
        if answer == 'h':
            end = guess - 1
        elif answer == 'l':
            start = guess + 1
        elif answer == 'c' or dictate:
            correct = True

    return (dictate, num_guesses)


guess_number_persist_results = persist_results(guess_number)
guess_number_accumulate = accumulate(guess_number)
