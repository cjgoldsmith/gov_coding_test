from chess.positions import possible_moves


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
