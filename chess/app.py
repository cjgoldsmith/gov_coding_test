import argparse

from chess.positions import possible_moves

DESCRIPTION = (
    "Given a chess piece and a board position, displays all possible positions ",
    "for that peice during the next move of play."
)

parser = argparse.ArgumentParser(
    description=DESCRIPTION)

parser.add_argument("--peice", type=str, required=True)
parser.add_argument("--position", type=str, required=True)

args = parser.parse_args()

if __name__ == '__main__':
    print(', '.join(possible_moves(args.peice, args.position)))
