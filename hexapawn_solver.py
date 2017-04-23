#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Hexapawn solver

Given a string board state (from redirected stdin), determine the value. The
possible values are 1 (piece on move wins) or -1 (opponent wins). There are
no games that end in a draw in hexapawn. The board state will look something
like this:

    B
    ppp
    .P.
    P.P

Where the first character, 'B' in this case, is the color on move. Each 'p'
represents a black pawn and each 'P' represents a white pawn. The input sizes
will be no larger than 8x8. There will be at least 1 and no more than n pawns
where n is the width of the board.
"""

# Imports
from hexapawn.piece import Pawn
from hexapawn.state import State
import numpy as np
import sys
import log
import argparse

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Hexapawn Solver')
    parser.add_argument('-f', '--filename', required=False, dest='filename',
                        help='Filename of the text version of the hexapawn board')
    parser.add_argument('--debug', help='Turn on debugging mode', action='store_true')
    args = parser.parse_args()

    logger = log.setup_custom_logger('root', args.debug)

    if args.filename:
        with open(args.filename, 'r') as f:
            state = State(f.read())
    else:
        state = State(sys.stdin.read())
