from chess.positions import ChessPeice, possible_moves


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


def test_all_rook():
    for square in all_squares():
        possible_moves('Rook', square)


def test_all_queen():
    for square in all_squares():
        possible_moves('Queen', square)


def test_all_knight():
    for square in all_squares():
        possible_moves('Knight', square)
