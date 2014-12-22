from __future__ import absolute_import, print_function
import six
import sys
import os
from os import path
from zipfile import ZipFile

from clint.textui import progress
from .helpers import print_notice
from .helpers import print_success
from .helpers import print_error
from .helpers import print_list
from .helpers import isatty

from . import updaters


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"
LATEST_ZIP = "latest.zip"



class _CacheResolver(object):
    PROGRAM_CACHE = ".genignore_cache"
    LATEST_ZIP = "latest.zip"

    def get_cache_paths(self):
        folder = path.join(path.expanduser("~"), self.PROGRAM_CACHE)
        return folder, LATEST_ZIP

    def get_latest_file(self):
        folder, filename = self.get_cache_paths()
        return path.join(folder, filename)

    def get_templates_from_zipfile(self, latest_file):

        templates = dict()

        with ZipFile(latest_file, 'r') as latest:
            for zi in latest.infolist():
                name = path.split(zi.filename)[-1].split(".")[0].lower()
                if len(name):
                    templates[name] = zi.filename

        return templates

    def init_repo_templates(self, sync=None):

        folder, filename = self.get_cache_paths()
        latest_file = self.get_latest_file()
        dir_exists = path.isdir(folder)
        file_missing = not os.path.isfile(latest_file)

        if not dir_exists:
            print_notice("github template folder not found. Creating folder at %s" % folder)
            file_missing = True
            os.makedirs(folder)

        if file_missing or sync:
            update_latest_from_github(MASTER_ARCHIVE, latest_file)

        return self.get_templates_from_zipfile(latest_file)


class GenController(object):

    def __init__(self):
        self.resolver = _CacheResolver()

    def gen(self, args):
        given_names = [n.lower().strip() for n in args.names]

        templates = self.resolver.init_repo_templates()
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
        build_gitignore(self.resolver, selected, out=out,
                        add_to_existing=args.add, original_templates=templates)
        return 0

    def sync(self, args):
        self.resolver.init_repo_templates(sync=True)
        return 0

    def list(self, args):
        templates = self.resolver.init_repo_templates()
        print_list(templates.keys(), title='Available Templates:')
        return 0

    def __call__(self, args):
        action = args.action
        if hasattr(self, action):
            return getattr(self, action)(args)
        else:
            raise NotImplementedError()

def update_latest_from_github(archive_uri, latest_file):

    print_notice("Fetching latest template(s) from %s to %s" % (archive_uri, latest_file))
    downloader = updaters.get('github')(archive_uri, latest_file)
    total_length = next(downloader)

    if total_length:
        with progress.Bar(label="Downloading ", expected_size=int(total_length)) as bar:
            for downloaded in downloader:
                bar.show(downloaded)

    print_success("Done!")




def build_gitignore(resolver, templates_for_merging, out=None, add_to_existing=False, original_templates={}):

    def make_separator(name, end=''):
        parts = [os.linesep, "# ", "<", end, "genignore ", name, ">", os.linesep]
        return "".join(parts)

    def extract_separator(line):
        res = line.replace("# <genignore ", "").replace(">", "")
        return res.strip()

    file_content = []
    existing_templates = []

    fname = path.join(*resolver.get_cache_paths())

    # find the file we want to load
    if out is sys.stdout or len(out) == 0:
        cwd = os.getcwd()
        gitignore_path = path.join(cwd, ".gitignore")
    else:
        gitignore_path = path.realpath(out)

    # collect existing genignore tags and orphan entries
    if os.path.isfile(gitignore_path):
        print_notice("file %s exists. Getting content..." % gitignore_path)
        with open(gitignore_path) as f:

            pushlines = True
            for line in f:
                if "# <genignore " in line:
                    existing_templates.append(extract_separator(line))
                    pushlines = False
                elif "# </genignore" in line:
                    pushlines = True
                else:
                    stripped_line = line.strip()
                    if pushlines and len(stripped_line):
                        file_content.append(stripped_line)

    if len(existing_templates):
        print_notice("file %s was generated by genignore. Found the following templates" % gitignore_path)
        print_list(existing_templates)
        if add_to_existing:
            print_notice("These will be added to the existing templates")
            for t in existing_templates:
                if t in original_templates:
                    templates_for_merging[t] = original_templates[t]
                else:
                    print_notice("Warning: template %s not found. Skipping..." % t)
        else:
            print_notice("Warning: will not add to existing file. Use --add to add these...")
            for e in existing_templates:
                if e in templates_for_merging:
                    del templates_for_merging[e]

    if len(templates_for_merging):
        print_notice("building .gitignore for (%s)" % ", ".join(templates_for_merging.keys()))

        with ZipFile(fname, 'r') as zipfile:
            for name, template in templates_for_merging.iteritems():
                with zipfile.open(template, 'rU') as tmp:
                    file_content.append(make_separator(name))
                    file_content.append(tmp.read())
                    file_content.append(make_separator(name, "/"))

        file_content.append(os.linesep)
        gitignore = os.linesep.join(file_content)
        if out is sys.stdout:
            out.write(gitignore)
        else:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore)
                print_success("Done writing .gitignore templates on file %s" % gitignore_path)
    else:
        print_notice("no templates remaining after filtering. Exiting")

