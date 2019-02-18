'''A utility module that helps with terminal manipulation'''

import sys


def clear_line():
    '''Clears all the text on the current line'''
    sys.stdout.write('\x1b[2K\r')


def move_line_up():
    '''Moves the terminal cursor up one line'''
    sys.stdout.write('\033[F')


def move_line_down():
    '''Moves the terminal cursor down one line'''
    sys.stdout.write('\n')
