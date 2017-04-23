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

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

import logging

import numpy as np
from typing import Tuple, List

import hexapawn.state


class Piece:
    def __init__(self, color: str, board_size: Tuple[int, int]):
        self.logger = logging.getLogger('hexapawn.piece.Piece')
        self.logger.setLevel(logging.DEBUG)
        self.color = color
        self.board_height, self.board_width = board_size


class Pawn(Piece):
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
            self.logger.debug('\n    anchor[0]: {}\n'
                              'anchor[0] + 2: {}\n'
                              'anchor[1] - 1: {}\n'
                              'anchor[1] + 2: {}'.format(self.anchor[0], self.anchor[0] + 2, self.anchor[1] - 1,
                                                         self.anchor[1] + 2))
            self.move_mask[self.anchor[0]:self.anchor[0] + 2, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                         [0, 1, 0]]
            self.logger.debug("Pawn('B', {}).move_mask: {}".format(board_size, self.move_mask))
            self.attack_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.attack_mask[self.anchor[0]:self.anchor[0] + 2, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                           [1, 0, 1]]
            self.logger.debug("Pawn('B', {}).attack_mask: {}".format(board_size, self.attack_mask))
        else:  # color == 'W'
            self.label = 'P'
            self.adversary_label = 'p'
            self.anchor = (self.mask_height // 2, self.mask_width // 2)
            self.logger.debug("Pawn('W', {}).anchor: {}".format(board_size, self.anchor))
            self.move_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.logger.debug("Pawn('W', {}).move_mask: {}".format(board_size, self.move_mask))
            self.logger.debug('\nanchor[0] - 1: {}\n'
                              'anchor[0] + 1: {}\n'
                              'anchor[1] - 1: {}\n'
                              'anchor[1] + 2: {}'.format(self.anchor[0] - 1, self.anchor[0] + 1, self.anchor[1] - 1,
                                                         self.anchor[1] + 2))
            self.move_mask[self.anchor[0] - 1:self.anchor[0] + 1, self.anchor[1] - 1:self.anchor[1] + 2] += [[0, 1, 0],
                                                                                                             [0, 1, 0]]
            self.attack_mask = np.zeros((self.mask_height, self.mask_width), dtype=np.int)
            self.attack_mask[self.anchor[0] - 1:self.anchor[0] + 1, self.anchor[1] - 1:self.anchor[1] + 2] += [
                [1, 0, 1],
                [0, 1, 0]]

    def get_move_masks(self, board_location: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
        top, left = self.anchor[0] - board_location[0], self.anchor[1] - board_location[1]
        return self.move_mask[top:top + self.board_height, left:left + self.board_width], self.attack_mask[
                                                                                          top:top + self.board_height,
                                                                                          left:left + self.board_width]

    def get_moves(self, state: hexapawn.state.State) -> Tuple[
        List[Tuple[np.ndarray, np.ndarray]], List[Tuple[np.ndarray, np.ndarray]]]:
        assert state.turn == self.color

        attacks = []
        moves = []

        for position in state.on_move_locations:
            move_mask, attack_mask = self.get_move_masks(position)
            attacks += [(position, move) for move in np.argwhere((attack_mask & state.adversary_mask) == 1)]
            moves += [(position, move) for move in np.argwhere((move_mask & state.empty_cells_mask) == 1)]

        return (attacks, moves)


if __name__ == '__main__':
    import sys

    for key in sys.modules.keys():
        print(key)
