import sys
import os
from os import path
import argparse
import requests
from zipfile import ZipFile

from clint.textui import puts, progress
from clint.textui import columns, colored


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"
LATEST_ZIP = "latest.zip"

TTY_COLUMN_SIZE = 80


def print_colored(txt, color):
    if sys.stdout.isatty():
        puts(color(txt))


print_error = lambda txt: print_colored(txt, colored.red)
print_notice = lambda txt: print_colored(txt, colored.yellow)
print_success = lambda txt: print_colored(txt, colored.green)


def parse(args):
    parser = argparse.ArgumentParser(description="Generates .gitignore files")
    subparsers = parser.add_subparsers(title='subcommands',
                                       help='valid genignore subcommands',
                                       dest="action")

    gen_parser = subparsers.add_parser('gen', help='generate a gitignore')


    gen_parser.add_argument('names', metavar='N', type=str, nargs='+',
                            help='Name(s) of things to include to the .gitignore')

    gen_parser.add_argument("-o", "--out", type=str, default='',
                            help='file to output the generated gitignore (default .gitignore of pwd)')

    gen_parser.add_argument("--update", action='store_true',
                            help='update the file if it exists, keeping custom entries')


    sync_parser = subparsers.add_parser("sync", help='sync to latest templates (requires internet connection)')

    list_parser = subparsers.add_parser("list", help="list all available templates")

    return parser.parse_args(args)


def get_cache_paths():
    folder = path.join(path.expanduser("~"), GENIGNORE_CACHE)
    return folder, LATEST_ZIP


def get_latest_file():
    folder, filename = get_cache_paths()
    return path.join(folder, filename)


def get_templates_from_zipfile(latest_file):

    templates = dict()

    with ZipFile(latest_file, 'r') as latest:
        for zi in latest.infolist():
            name = path.split(zi.filename)[-1].split(".")[0].lower()
            if len(name):
                templates[name] = zi.filename

    return templates


def update_latest_from_github(latest_file):

    print_notice("Fetching latest templates from %s" % MASTER_ARCHIVE)

    response = requests.get(MASTER_ARCHIVE, stream=True)
    total_length = response.headers.get('content-length')

    with open(latest_file, "wb") as f:
        if total_length:
            dl = 0
            with progress.Bar(label="Downloading ", expected_size=int(total_length)) as bar:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    dl += len(chunk)
                    bar.show(dl)
        else:
           f.write(response.content)

    print_success("Done!")


def init_repo_templates(sync=None):

    folder, filename = get_cache_paths()
    latest_file = get_latest_file()
    dir_exists = path.isdir(folder)
    file_missing = not os.path.isfile(latest_file)

    if not dir_exists:
        print_notice("github template folder not found. Creating folder at %s" % folder)
        file_missing = True
        os.makedirs(folder)

    if file_missing or sync:
        update_latest_from_github(latest_file)

    return get_templates_from_zipfile(latest_file)


def make_separator(name, end=''):
    parts = [os.linesep, "# ", "<", end, "genignore ", name, ">", os.linesep]
    return "".join(parts)


def build_gitignore(templates_for_merging, out=None):

    print_notice("building .gitignore for (%s)" % ", ".join(templates_for_merging.keys()))

    file_content = []
    fname = path.join(*get_cache_paths())

    with ZipFile(fname, 'r') as zipfile:
        for name, template in templates_for_merging.iteritems():
            with zipfile.open(template, 'rU') as tmp:
                file_content.append(make_separator(name))
                file_content.append(tmp.read())
                file_content.append(make_separator(name, "/"))

    if out is sys.stdout or len(out) == 0:
        cwd = os.getcwd()
        gitignore_path = path.join(cwd, ".gitignore")
    else:
        gitignore_path = path.realpath(out)

    if os.path.isfile(gitignore_path):
        print_notice("file %s exists. Updating..." % gitignore_path)
        with open(gitignore_path) as f:

            pushlines = True
            for line in f:
                if "# <genignore " in line:
                    pushlines = False
                elif "# </genignore" in line:
                    pushlines = True
                else:
                    stripped_line = line.strip()
                    if pushlines and len(stripped_line):
                        file_content.append(stripped_line)

    file_content.append(os.linesep)
    gitignore = os.linesep.join(file_content)
    if out is sys.stdout:
        out.write(gitignore)
    else:
        with open(gitignore_path, 'w') as f:
            f.write(gitignore)
            print_success("Done writing .gitignore templates on file %s" % gitignore_path)


def list_templates(names):
    print_notice('Available Templates:')
    puts(columns([", ".join(names), TTY_COLUMN_SIZE]))


def main(arguments):
    args = parse(arguments)
    action = args.action

    if action == "gen":
        given_names = [n.lower().strip() for n in args.names]

        templates = init_repo_templates()
        names = templates.keys()

        selected = dict()
        for n in given_names:
            if n in names:
                selected[n] = templates[n]
            else:
                print_error("No .gitignore template available for %s." % n)
                print_notice("You can view available templates by running `genignore list`")

                return 1

        if sys.stdout.isatty():
            out = args.out
        else:
            out = sys.stdout
        build_gitignore(selected, out=out)

    elif action == "sync":
        init_repo_templates(sync=True)

    elif action == "list":
        templates = init_repo_templates()
        names = templates.keys()
        list_templates(names)

    return 0


def main_func():
    exit(main(sys.argv[1:]))


if __name__ == '__main__':
    main_func()
