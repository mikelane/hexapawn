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

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

import numpy as np
import logging
from typing import Union, Tuple
from hexapawn import piece
import re

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
            self.board = list(self.state_string.replace('\n', ''))
            self.turn, self.board = self.board[0][0], np.array(self.board[1:]).reshape(3, 3)
        elif type(state) == np.ndarray:
            try:
                assert turn != None and type(turn) == str and turn in 'WB'
            except AssertionError as e:
                self.logger.error('Assertion error in State constructor: {}'.format(e))
                raise e
            self.turn = turn
            self.board = state
        else:
            self.logger.error('State constructor called with something other than a str or np.ndarray!')
            assert False
        # TODO: build str representation
        self.opponent = 'W' if self.turn == 'B' else 'B'
        self.value = None
        self.on_move_pieces = [piece.Pawn(self.turn, self.board.shape)]

        self.empty_cells_mask = (self.board == '.').astype(np.int)
        if self.turn == 'W':
            self.on_move_locations = np.argwhere(self.board == 'P')
            self.adversary_mask = (self.board == 'p').astype(np.int)
            self.win_row = 0
        else:
            self.on_move_locations = np.argwhere(self.board == 'p')
            self.adversary_mask = (self.board == 'P').astype(np.int)
            self.win_row = -1

        self.attacks = []
        self.moves = []

        for piece_object in self.on_move_pieces:
            attacks, moves = piece_object.get_moves(self)
            if len(attacks) + len(moves) == 0:
                self.value = -1

    def apply_move(self, on_move_piece: piece, move: Tuple[np.ndarray, np.ndarray]) -> Tuple['State', int]:
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
        self.board[move[0]] = '.'
        self.board[move[1]] = on_move_piece.label
        return State(self.board, self.opponent), np.any(self.board[self.win_row] == on_move_piece.label).astype(np.int)


if __name__ == '__main__':
    import sys

    for key in sys.modules.keys():
        print(key)
