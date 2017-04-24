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

import argparse
import sys
from datetime import datetime
from functools import lru_cache

import log
from hexapawn.state import State

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

parser = argparse.ArgumentParser(description='''Hexapawn Solver: This script can handle inputs that come from the 
command line or from inputs that come from redirected stdin. Please ensure that you are using a python3 interpreter.''')
parser.add_argument('-f', '--filename', required=False, dest='filename',
                    help='Filename of the text version of the hexapawn board')
parser.add_argument('--debug', help='Turn on debugging mode', action='store_true')
parser.add_argument('-v', '--verbosity', action='count', default=0,
                    help='Increase output verbosity, blank shows ERROR only, '
                         '-v shows INFO and ERROR, -vv shows WARNING, INFO, and ERROR, and '
                         '-vvv shows all logs')
args = parser.parse_args()

if args.debug:
    logger = log.setup_custom_logger('root', level=5)
else:
    logger = log.setup_custom_logger('root', level=args.verbosity)

nodes = 0
my_cache_hits = 0

# Cache the mirror image. If mirror image states aren't used, this slows things down.
# However, when there are mirror image states to consider, this speeds things up greatly.
cache = {}


@lru_cache(maxsize=None)  # Automagical
def get_state_value(state: State) -> int:
    global nodes
    global cache
    global my_cache_hits
    if state.mirror() in cache:
        my_cache_hits += 1
        return cache[state.mirror()]

    if len(state.moves) == 0:
        cache[state] = cache[state.mirror()] = -1
        return -1

    max_value = -1

    for move in state.attacks + state.moves:
        new_state, result = state.apply_move(move)
        nodes += 1

        if result == 1:
            logger.debug('Found a win, returning 1')
            cache[new_state] = cache[new_state.mirror()] = 1
            return 1
        logger.debug('Win not found, continuing')

        val = -get_state_value(new_state)
        max_value = max(max_value, val)
    cache[state] = cache[state.mirror()] = max_value
    return max_value


if __name__ == '__main__':
    if args.filename:
        with open(args.filename, 'r') as f:
            state = State(f.read())
    else:
        state = State(sys.stdin.read())

    nodes += 1

    start = datetime.now()
    result = get_state_value(state)
    print(result)
    logger.warning(get_state_value.cache_info())
    logger.warning('my cache hits: {}'.format(my_cache_hits))
    logger.warning('{} Nodes :: {} seconds'.format(nodes, (datetime.now() - start).total_seconds()))
