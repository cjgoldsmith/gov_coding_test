from functools import partial

from chess.positions import ChessPeice, possible_moves

import pytest


def all_squares():
    for r in range(ChessPeice.BOARD_ROW_MAX - ChessPeice.BOARD_ROW_MIN + 1):
        for c in range(ChessPeice.BOARD_ROW_MAX - ChessPeice.BOARD_ROW_MIN + 1):
            row = ChessPeice.BOARD_ROW_MIN + r
            col = chr(ord(ChessPeice.BOARD_COLUMN_MIN) + c)
            yield col + str(row)


def test_rook_position():
    results = list(possible_moves('Rook', 'A8'))
    assert 'A8' not in results
    assert 'H8' in results
    assert 'A1' in results


def test_queen_position():
    results = list(possible_moves('Queen', 'B7'))
    assert 'B7' not in results
    assert 'A5' not in results
    assert 'A8' in results
    assert 'H7' in results
    assert 'H1' in results


def test_knight_position():

    # Middle of board
    results = list(possible_moves('Knight', 'E4'))
    assert len(results) == 8
    assert 'G5' in results
    assert 'C3' in results

    # Edge of board
    results = list(possible_moves('Knight', 'H5'))
    assert len(results) == 4
    assert 'F6' in results
    assert 'G3' in results


def _test_all(type):
    for square in all_squares():
        possible_moves(type, square)


test_all_rook = partial(_test_all, 'Rook')
test_all_queen = partial(_test_all, 'Queen')
test_all_knight = partial(_test_all, 'Knight')


def test_chess_peice_validate_square_token():
    with pytest.raises(ValueError):
        ChessPeice.validate_square_token('G99')

    with pytest.raises(ValueError):
        ChessPeice.validate_square_token('I8')

    with pytest.raises(ValueError):
        ChessPeice.validate_square_token('H9')

    assert ChessPeice.validate_square_token('h8') == 'H8'


def test_chess_peice_tokenize_square():
    assert ChessPeice._tokenize_square('h8') == ('H', 8)


def test_chess_peice_is_square():
    assert not ChessPeice.is_square('I', 8)
    assert ChessPeice.is_square('H', 8)
