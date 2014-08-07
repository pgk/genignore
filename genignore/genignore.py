import sys
import os
from os import path
import argparse
import requests
from zipfile import ZipFile


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"
LATEST_ZIP = "latest.zip"


def parse(args):
    parser = argparse.ArgumentParser(description="Generates .gitignore files")
    parser.add_argument('names', metavar='N', type=str, nargs='+',
                        help='Name(s) of things to include to the .gitignore')
    parser.add_argument("-o", "--out", type=str,
                        default='',
                        help='where to output the generated gitignore')
    return parser.parse_args(args)


def get_cache_paths():
    folder = path.join(path.expanduser("~"), GENIGNORE_CACHE)
    return folder, LATEST_ZIP


def init_repo_templates():
    templates = None
    templates = dict()

    folder, filename = get_cache_paths()
    latest_file = path.join(folder, filename)
    if not path.isdir(folder):
        os.makedirs(folder)
        r = requests.get(MASTER_ARCHIVE, stream=True)
        with open(latest_file, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    with ZipFile(latest_file, 'r') as latest:
        for zi in latest.infolist():
            name = path.split(zi.filename)[-1].split(".")[0].lower()
            if len(name):
                templates[name] = zi.filename

    return templates


def build_gitignore(templates_for_merging, out=None):

    def make_separator(name, end=''):
        parts = [os.linesep, "# ", "<", end, "genignore ", name, ">", os.linesep]
        return "".join(parts)

    file_content = []
    fname = path.join(*get_cache_paths())

    with ZipFile(fname, 'r') as zipfile:
        for name, template in templates_for_merging.iteritems():
            with zipfile.open(template, 'rU') as tmp:
                file_content.append(make_separator(name))
                file_content.append(tmp.read())
                file_content.append(make_separator(name, "/"))

    if len(out) == 0:
        cwd = os.getcwd()
        gitignore_path = path.join(cwd, ".gitignore")
    else:
        gitignore_path = path.realpath(out)

    with open(gitignore_path, 'w') as f:
        f.write(os.linesep.join(file_content))


def main(arguments):
    args = parse(arguments)
    given_names = [n.lower().strip() for n in args.names]

    templates = init_repo_templates()
    names = templates.keys()

    selected = dict()
    for n in given_names:
        if n in names:
            selected[n] = templates[n]
        else:
            print("No .gitignore template available for %s" % n)
            print("aborting")
            return 1

    build_gitignore(selected, out=args.out)

    return 0


def main_func():
    exit(main(sys.argv[1:]))


if __name__ == '__main__':
    main_func()
