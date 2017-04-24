import nose.tools
import numpy as np
import subprocess as sp

import hexapawn
import logging
import os

tests_logger = logging.getLogger('root')


def setup():
    tests_logger.debug('Setting Up')


def teardown():
    tests_logger.debug('Tearing Down')


def test_basic():
    tests_logger.debug('Running Tests')


def test_state_construct():
    tests_logger.debug('Testing the board constructor')
    with open('tests/test_input_1.txt', 'r') as f:
        b = hexapawn.state.State(f.read())
    assert b.turn == 'B'
    assert np.array_equal(b.board, np.array([['p', 'p', 'p'], ['.', 'P', '.'], ['P', '.', 'P']]))

    b = hexapawn.state.State('W\n...\nPpP\npPp\n')
    assert b.turn == 'W'
    assert np.array_equal(b.board, np.array([['.', '.', '.'], ['P', 'p', 'P'], ['p', 'P', 'p']]))
    print('END')


def test_get_move_masks():
    tests_logger.debug('Testing getting move masks for white')
    b = hexapawn.state.State('W\np.p\n.Pp\nP..\n')
    w = hexapawn.piece.Pawn('W', b.board.shape)
    attack, move = w.get_moves(b)
    valid_attack = [(np.array([1, 1]), np.array([0, 0])), (np.array([1, 1]), np.array([0, 2]))]
    valid_move = [(np.array([1, 1]), np.array([0, 1])), (np.array([2, 0]), np.array([1, 0]))]
    for a, b in zip(attack, valid_attack):
        assert np.array_equal(a[0], b[0])
        assert np.array_equal(a[1], b[1])
    for a, b in zip(move, valid_move):
        assert np.array_equal(a[0], b[0])
        assert np.array_equal(a[1], b[1])


def test_positions():
    path = 'tests/positions'
    data = {}
    with os.scandir(path) as files:
        for file in files:
            if '.out' in file.name:
                with open('{}/{}'.format(path, file.name), 'r') as f:
                    data['{}/{}'.format(path, file.name.replace('.out', '.in'))] = f.read()
    for fn, correct in data.items():
        yield check_correct, correct, fn


@nose.tools.timed(30)
def check_correct(correct_value, fn):
    with open(fn, 'r') as f:
        result = sp.run(['python3', '/Users/Mike/dev/hexapawn/hexapawn_solver.py', '-vv', '-f', fn], stdout=sp.PIPE)
        assert correct_value == result.stdout.decode()
