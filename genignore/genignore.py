import sys
import os
from os import path
import argparse
import requests
from zipfile import ZipFile
from StringIO import StringIO


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"
LATEST_ZIP = "latest.zip"


def parse(args):
    parser = argparse.ArgumentParser(description="Generates .gitignore files")
    parser.add_argument('names', metavar='N', type=str, nargs='+',
                        help='Name(s) of things to include to the .gitignore')
    return parser.parse_args(args)


def get_cache_paths():
    folder = path.join(path.expanduser("~"), GENIGNORE_CACHE)
    return folder, LATEST_ZIP


def init_repo_templates():
    templates = None
    names = dict()

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
                names[name] = zi.filename
        templates = names.keys()

    return templates, names


def make_gitignore(templates_for_merging):

    file_content = []
    fname = path.join(*get_cache_paths())
    print(fname)
    with ZipFile(fname, 'r') as zipfile:
        for name, template in templates_for_merging.iteritems():
            with zipfile.open(template, 'rU') as tmp:
                tmpl_separator = "".join([os.linesep, "# ", "<genignore ", name, ">", os.linesep])
                file_content.append(tmpl_separator)
                file_content.append(tmp.read())
                tmpl_separator = "".join([os.linesep, "# ", "</genignore ", name, ">", os.linesep])
                file_content.append(tmpl_separator)

    cwd = os.getcwd()
    gitignore_path = path.join(cwd,".gitignore")
    with open(gitignore_path, 'w') as f:
        f.write(os.linesep.join(file_content))

def main(arguments):
    args = parse(arguments)
    given_names = [n.lower().strip() for n in args.names]

    templates, names = init_repo_templates()

    templates_for_merging = dict()
    for n in given_names:
        if n in templates:
            templates_for_merging[n] = names[n]
        else:
            print("No .gitignore template available for %s" % n)
            print("aborting")
            return 1

    make_gitignore(templates_for_merging)

    return 0


main_func = lambda args: exit(main(args))


if __name__ == '__main__':
    main_func(sys.argv[1:])
