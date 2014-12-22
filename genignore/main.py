from __future__ import absolute_import, print_function
import sys

from genignore.cli import parse
from genignore.core import GenController


def main(arguments):
    controller = GenController()
    return controller(parse(arguments))


def main_func():
    exit(main(sys.argv[1:]))


if __name__ == '__main__':
    main_func()
