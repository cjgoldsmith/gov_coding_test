import argparse

from guess_number.guess import guess_number_accumulate
from guess_number.persist import AVERAGE, get_accumulated

DESCRIPTION = (
    "Play the guessing game, enter the maximum number (n),",
    " then tell your opponent if their guess is higher (h), lower (l),",
    " or correct (c)",
)
parser = argparse.ArgumentParser(
    description=DESCRIPTION)

args = parser.parse_args()

PERMITTED_INPUTS = ['l', 'h', 'c']
PERMITTED_YN_INPUTS = ['y', 'n']


def get_user_answer(guess):
    reply = ''
    while reply not in PERMITTED_INPUTS:
        reply = input(f'{guess}?').lower()
    return reply


if __name__ == '__main__':

    n_set = False
    while not n_set:
        try:
            n = int(input('Please enter a number n: '))
            n_set = True
        except ValueError:
            print('Invalid number, try again...')

    idx_game = 1
    while True:
        dictate, guess = guess_number_accumulate(0, n, get_user_answer)
        if dictate:
            print(f'Your number is {dictate}')
        print(f'It took me {guess} guesses')
        print(
            f'I averaged {int(get_accumulated()[AVERAGE])} guesses per game for {idx_game} games')

        again = ''
        while again not in PERMITTED_YN_INPUTS:
            again = input('Play again? (y/n)').lower()
        if again == 'n':
            break
        idx_game += 1
