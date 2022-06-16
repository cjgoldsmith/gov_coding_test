from chess.decorators import log_results

import structlog

log = structlog.get_logger()


class ChessPeice:

    KNIGHT = 'knight'
    ROOK = 'rook'
    QUEEN = 'queen'

    PEICES = [
        KNIGHT,
        ROOK,
        QUEEN,
    ]

    BOARD_ROW_MAX = 8
    BOARD_ROW_MIN = 1
    BOARD_COLUMN_MAX = 'H'
    BOARD_COLUMN_MIN = 'A'

    @classmethod
    def validate_square_token(cls, token):
        token = token.upper()
        if len(token) != 2:
            raise ValueError(f'token: {token} is not valid length')
        if (token[0] < cls.BOARD_COLUMN_MIN or token[0] > cls.BOARD_COLUMN_MAX):
            raise ValueError(f'token column value out of range {token}')
        if (int(token[1]) < cls.BOARD_ROW_MIN or int(token[1]) > cls.BOARD_ROW_MAX):
            raise ValueError(f'token row value out of range {token}')
        return token

    @classmethod
    def _tokenize_square(cls, square):
        square = cls.validate_square_token(square)
        return (square[0], int(square[1]))

    @classmethod
    def is_square(cls, column, row):
        try:
            cls.validate_square_token(column + str(row))
        except ValueError:
            return False
        return True


class Rook(ChessPeice):

    @classmethod
    @log_results
    def generate_moves(cls, square):
        square = square.upper()
        possible = []
        column, row = cls._tokenize_square(square)

        # All row moves
        for col in range(ord(cls.BOARD_COLUMN_MIN), ord(cls.BOARD_COLUMN_MAX) + 1):
            col = chr(col)
            possible.append(col + str(row))

        # All column moves
        for r in range(cls.BOARD_ROW_MIN, cls.BOARD_ROW_MAX + 1):
            possible.append(column + str(r))

        # Remove duplicate moves, current position, return
        return [pos for pos in set(possible) if pos != square]


class Queen(ChessPeice):

    rook = Rook()

    @classmethod
    @log_results
    def generate_moves(cls, square):
        square = square.upper()
        possible = []
        column, row = cls._tokenize_square(square)

        # Generate rook moves since they overlap with Queen
        possible += list(cls.rook.generate_moves(square))

        # Leverage the fact that boards are square, generate all diagonals
        # for the possible length of the board.
        for r in range(cls.BOARD_ROW_MAX - cls.BOARD_ROW_MIN):
            diagonals = [
                [chr(ord(column) + (r + 1)), row + (r + 1)],
                [chr(ord(column) + (r + 1)), row - (r + 1)],
                [chr(ord(column) - (r + 1)), row + (r + 1)],
                [chr(ord(column) - (r + 1)), row - (r + 1)],
            ]

            # Serialize the diagonal, filter out invalid move options
            diagonals = [d[0] + str(d[1])
                         for d in diagonals if cls.is_square(*d)]
            possible += diagonals
        return possible


class Knight(ChessPeice):

    MOVE_SET = (
        [2, 1],
        [2, -1],
        [1, 2],
        [1, -2],
        [-2, 1],
        [-2, -1],
        [-1, 2],
        [-1, -2],
    )

    @classmethod
    @log_results
    def generate_moves(cls, square):
        square = square.upper()
        column, row = cls._tokenize_square(square)

        # Generate all possible moves, even invalid ones
        knight_possible = map(
            lambda ms: [chr(ord(column) + ms[0]), row + ms[1]], cls.MOVE_SET)

        # Serialize moves and filter out invalid move options
        possible = [pos[0] + str(pos[1])
                    for pos in knight_possible if cls.is_square(*pos)]
        return possible


PEICE_MAP = {
    ChessPeice.ROOK: Rook,
    ChessPeice.QUEEN: Queen,
    ChessPeice.KNIGHT: Knight,
}


def possible_moves(peice, square):
    return PEICE_MAP[peice.lower()].generate_moves(square)
