import math
from functools import partial

import structlog
from guess_number.guess import guess_number_persist_results

log = structlog.get_logger()


def _test_guess(n):
    """
    Base test method, tests guess number functionality for all
    numbers 0 - n.
    """
    max_guesses = math.ceil(math.log2(n)) + 1
    for secret_number in range(n + 1):
        def answer(guess):
            if guess > secret_number:
                return 'h'
            elif guess < secret_number:
                return 'l'
            elif guess == secret_number:
                return 'c'

        _, guesses = guess_number_persist_results(0, n, answer)
        if guesses > max_guesses:
            log.msg('Maxinum number of guesses exceeded', n=n,
                    guesses=guesses, secret_number=secret_number, max_guesses=max_guesses)
            assert False
        else:
            log.msg('Successfully guessed', n=n,
                    guesses=guesses, secret_number=secret_number)


# Concrete test cases
test_100 = partial(_test_guess, 100)
test_250 = partial(_test_guess, 250)
test_4 = partial(_test_guess, 4)
test_2 = partial(_test_guess, 2)
