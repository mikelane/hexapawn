#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""State Class

This manages the game state. For hexapawn, the game state is the player that is
on turn (B or W) and the location of the pawns on the board. The constructor does
a lot of work up front which means the algorithm given in class must be changed
slightly. 

Both the game state and the piece/pawn classes make extensive use of numpy. I'm
hoping that numpy will have a ease and speed benefit over lists and an ease benefit
over bit strings and won't be the worst of both worlds.
"""

# Imports
import logging
import re

import numpy as np
from typing import Union, Tuple

from hexapawn import piece

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class State:
    def __init__(self, state: Union[str, np.ndarray], turn: str = None):
        """
        State constructor. Pass it a string as in the project description or pass it a
        numpy array board and a turn.
        Parameters
        ----------
        state - Either a str or a numpy array
        turn  - Ignored if state is a string, required if state is a numpy array. Must
                be either 'B' for black or 'W' for white.
        """
        self.logger = logging.getLogger('root')

        if type(state) == str:
            self.logger.debug(state)
            self.logger.debug(re.search(r'([B|W]{1})\n(([p|P|.]{3,8})\n){3,8}', state))
            assert re.search(r'([B|W]{1})\n(([p|P|.]{3,8})\n){3,8}', state)
            self.logger.debug('Valid state, continuing')

            self.state_string = state
            self.turn, *self.board = state.strip().split('\n')
            self.board = np.array([list(row) for row in self.board])
        elif type(state) == np.ndarray:
            try:
                assert turn != None and type(turn) == str and turn in 'WB'
            except AssertionError as e:
                self.logger.critical('Assertion error in State constructor: {}'.format(e))
                raise e
            self.turn = turn
            self.board = state
        else:
            self.logger.critical('State constructor called with something other than a str or np.ndarray!')
            assert False
        self.opponent = 'W' if self.turn == 'B' else 'B'
        self.value = None
        self.on_move_pieces = [piece.Pawn(self.turn, self.board.shape)]

        self.empty_cells_mask = (self.board == '.').astype(np.int)
        if self.turn == 'W':
            self.on_move_label = 'P'
            self.adversary_label = 'p'
            self.win_row = 0
        else:
            self.on_move_label = 'p'
            self.adversary_label = 'P'
            self.win_row = -1

        self.on_move_locations = np.argwhere(self.board == self.on_move_label)
        self.adversary_mask = (self.board == self.adversary_label).astype(np.int)

        self.attacks = []
        self.moves = []

        for piece_object in self.on_move_pieces:
            self.attacks, self.moves = piece_object.get_moves(self)
            if len(self.attacks) + len(self.moves) == 0:
                self.value = -1

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __ne__(self, other):
        return not np.array_equal(self.board, other.board)

    def mirror(self):
        return State(np.fliplr(self.board), self.turn)

    def apply_move(self, move: Tuple[np.ndarray, np.ndarray]) -> Tuple['State', int]:
        """
        Apply single move to a board and if the result was a win
        Parameters
        ----------
        on_move_piece - A piece object of the type and color to be moved.
        move          - A starting position and ending position for the piece.

        Returns
        -------
        Tuple of new board state and 1 if a win has been detected or a 0 otherwise.

        """
        board = np.copy(self.board)
        self.logger.debug(
            'Applying {} move {} to label {} on board:\n{}'.format(self.turn, move, self.on_move_label, board))
        self.logger.debug('tuple(move[0]): {}, board[tuple(move[0])]: {}'.format(tuple(move[0]), board[tuple(move[0])]))
        board[tuple(move[0])] = '.'
        board[tuple(move[1])] = self.on_move_label
        self.logger.info('Updated board: \n{}'.format(board))
        return State(board, self.opponent), np.any(board[self.win_row] == self.on_move_label).astype(np.int)


if __name__ == '__main__':
    import sys

    for key in sys.modules.keys():
        print(key)
