from __future__ import absolute_import, print_function
import sys

from .helpers import isatty
from .helpers import print_notice

from .cli import parse
from .core import GenController


splash_screen = """\
genignore v1.0.1
----------------"""


def main(arguments):
    if isatty():
        print_notice(splash_screen)
    controller = GenController()
    controller(parse(arguments))

    return 0


def main_func():
    exit(main(sys.argv[1:]))


if __name__ == '__main__':
    main_func()
