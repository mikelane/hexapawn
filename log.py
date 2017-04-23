#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Set up the logging environment

Copied from Stack Overflow:
http://stackoverflow.com/questions/7621897/python-logging-module-globally"""

# Imports
import logging

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


def setup_custom_logger(name:str, debug:bool) -> logging.Logger:
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name=name)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger
