#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Hexapawn Piece

The Piece class and the Pawn subclass handle the hexapawn pawns. The constructor handles
the initialization of the various sizes and masks for a given board size. All this work
isn't strictly required and the subclassing, frankly, doesn't make a lick of sense for
this problem. I'm building an infrastructure that I can use for a minichess AI where these
classes will make a lot more sense.
"""

# Imports
import logging

import numpy as np
from typing import Tuple, List

import hexapawn.state

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class Piece:
    """
    The Piece class. A Piece has a color and is played on a specific board type.
    """

    def __init__(self, color: str, board_size: Tuple[int, int]):
        self.logger = logging.getLogger('root')
        self.color = color
        self.board_height, self.board_width = board_size


class Pawn(Piece):
    """
    A Pawn is a specific type of piece. Each piece has its own unique move mask. The mask is set up such
    that the piece mask will span the entire board no matter where the location of the piece on the board
    is. For pawns, most locations will be 0, but this is fine since the move generation is being done via
    a logical AND mask. The 0's are all the locations the pawn can't reach, so they shouldn't be
    considered when generating moves anyhow.
    """

    def __init__(self, color, board_size):
        super().__init__(color, board_size)
        self.mask_height = 2 * (self.board_height - 1)
        self.mask_width = 2 * self.board_width - 1
        if color == 'B':
            self.label = 'p'
            self.adversary_label = 'P'
            self.anchor = (self.mask_height // 2 - 1, self.mask_width // 2)
            self.logger.debug("Pawn('B', {}).anchor: {}".format(board_size, self.anchor))
            self.move_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.logger.debug('move_mask slice: ({}:{}, {}:{})'.format(self.anchor[0],
                                                                       self.anchor[0] + 2,
                                                                       self.anchor[1] - 1,
                                                                       self.anchor[1] + 2))
            self.move_mask[self.anchor[0]:self.anchor[0] + 2, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                         [0, 1, 0]]
            self.logger.debug("Pawn('B', {}).move_mask: \n{}".format(board_size, self.move_mask))
            self.attack_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)

            self.logger.debug('attack_mask slice: ({}:{}, {}:{})'.format(self.anchor[0],
                                                                         self.anchor[0] + 2,
                                                                         self.anchor[1] - 1,
                                                                         self.anchor[1] + 2))
            self.attack_mask[self.anchor[0]:self.anchor[0] + 2, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                           [1, 0, 1]]
            self.logger.debug("Pawn('B', {}).attack_mask: \n{}".format(board_size, self.attack_mask))
        else:  # color == 'W'
            self.label = 'P'
            self.adversary_label = 'p'
            self.anchor = (self.mask_height // 2, self.mask_width // 2)
            self.logger.debug("Pawn('W', {}).anchor: {}".format(board_size, self.anchor))
            self.move_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.logger.debug('move_mask slice: ({}:{}, {}:{})'.format(self.anchor[0] - 1,
                                                                       self.anchor[0] + 1,
                                                                       self.anchor[1] - 1,
                                                                       self.anchor[1] + 2))
            self.move_mask[self.anchor[0] - 1:self.anchor[0] + 1, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                             [0, 1, 0]]
            self.logger.debug("Pawn('W', {}).move_mask: \n{}".format(board_size, self.move_mask))

            self.attack_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.logger.debug('attack_mask slice: ({}:{}, {}:{})'.format(self.anchor[0] - 1,
                                                                         self.anchor[0] + 1,
                                                                         self.anchor[1] - 1,
                                                                         self.anchor[1] + 2))
            self.attack_mask[self.anchor[0] - 1:self.anchor[0] + 1, self.anchor[1] - 1:self.anchor[1] + 2] += \
                [[1, 0, 1],
                 [0, 1, 0]]
            self.logger.debug("Pawn('W', {}).attack_mask: \n{}".format(board_size, self.attack_mask))

    def __hash__(self):
        return hash(self.color + str(self.move_mask | self.attack_mask))

    def __eq__(self, other):
        return self.color == other.color and np.array_equal(self.attack_mask | self.attack_mask,
                                                            other.attack_mask | other.move_mask)

    def get_move_masks(self, board_location: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
        top, left = self.anchor[0] - board_location[0], self.anchor[1] - board_location[1]
        return self.move_mask[top:top + self.board_height, left:left + self.board_width], self.attack_mask[
                                                                                          top:top + self.board_height,
                                                                                          left:left + self.board_width]

    # @lru_cache(maxsize=None)
    def get_moves(self, state: hexapawn.state.State) -> Tuple[
        List[Tuple[np.ndarray, np.ndarray]], List[Tuple[np.ndarray, np.ndarray]]]:
        assert state.turn == self.color

        attacks = []
        moves = []

        for position in state.on_move_locations:
            move_mask, attack_mask = self.get_move_masks(tuple(position))
            # Numpy's argwhere returns a lists of locations where some comparison is true in a
            # list from top left to bottom right of the 2D array. If the piece is moving north
            # to south, you'd want to check the bottom row first. That is what flipud() does.
            if state.turn == 'B':
                attacks += [(position, move) for move in
                            np.flipud(np.argwhere((attack_mask & state.adversary_mask) == 1))]
            else:  # Moving south to north, the normal argwhere return value is fine.
                attacks += [(position, move) for move in np.argwhere((attack_mask & state.adversary_mask) == 1)]

            moves += [(position, move) for move in np.argwhere((move_mask & state.empty_cells_mask) == 1)]

        return (attacks, moves)


if __name__ == '__main__':
    import sys

    for key in sys.modules.keys():
        print(key)
