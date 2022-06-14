from .guess_number import guess_number
from functools import partial

import math
import structlog

log = structlog.get_logger()


def test_hello():
    print('test hello')
    assert True


def _test_guess(n):
    for secret_number in range(n + 1):
        def answer(guess):
            if guess > secret_number:
                return 'h'
            elif guess < secret_number:
                return 'l'
            elif guess == secret_number:
                return 'c'

        guesses = guess_number(0, n, answer)
        if guesses > (math.log2(n) + 1):
            log.msg('Maxinum number of guesses exceeded', n=n,
                    guesses=guesses, secret_number=secret_number)
            assert False
        else:
            log.msg('Successfully guessed', n=n,
                    guesses=guesses, secret_number=secret_number)


test_100 = partial(_test_guess, 100)
test_1000 = partial(_test_guess, 1000)
test_4 = partial(_test_guess, 4)
