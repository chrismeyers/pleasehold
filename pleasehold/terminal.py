import sys


def clear_line():
    sys.stdout.write('\x1b[2K\r')


def move_line_up():
    sys.stdout.write('\033[F')


def move_line_down():
    sys.stdout.write('\n')
