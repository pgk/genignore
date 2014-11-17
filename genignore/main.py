from __future__ import absolute_import, print_function
import sys
import os
from os import path
from zipfile import ZipFile

from clint.textui import progress
from .helpers import print_colored
from .helpers import print_error
from .helpers import print_notice
from .helpers import print_success
from .helpers import isatty
from .helpers import print_list

from .cli import parse
from . import updaters


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"
LATEST_ZIP = "latest.zip"


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


def update_latest_from_github(archive_uri, latest_file):

    print_notice("Fetching latest template(s) from %s" % archive_uri)
    downloader = updaters.get('github')(archive_uri, latest_file)
    total_length = next(downloader)

    if total_length:
        with progress.Bar(label="Downloading ", expected_size=int(total_length)) as bar:
            for downloaded in downloader:
                bar.show(downloaded)

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
        update_latest_from_github(MASTER_ARCHIVE, latest_file)

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

        if isatty():
            out = args.out
        else:
            out = sys.stdout
        build_gitignore(selected, out=out)

    elif action == "sync":
        init_repo_templates(sync=True)

    elif action == "list":
        templates = init_repo_templates()
        names = templates.keys()
        print_list(names, title='Available Templates:')

    return 0


def main_func():
    exit(main(sys.argv[1:]))


if __name__ == '__main__':
    main_func()
