import sys
from clint.textui import puts
from clint.textui import colored
from clint.textui import progress
from clint.textui import columns


TTY_COLUMN_SIZE = 80


isatty = lambda : sys.stdout.isatty()


def print_colored(txt, color):
    if isatty():
        puts(color(txt))


print_error = lambda txt: print_colored(txt, colored.red)

print_notice = lambda txt: print_colored(txt, colored.yellow)

print_success = lambda txt: print_colored(txt, colored.green)


def print_list(names, title=None):
    if title:
        print_notice('Available Templates:')
    puts(columns([", ".join(names), TTY_COLUMN_SIZE]))
