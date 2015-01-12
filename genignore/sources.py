from os.path import isdir, realpath
from .config import GENIGNORE_CACHE

class Source(object):

    def __init__(self, path, target=None):
        super(Source, self).__init__()

        self.isdir = False
        self.local_path = None
        self.type, self.path = path.split('://')
        self.ns = ''
        self.items = {}

        assert self.type in ('file', 'http', 'https')

        if self.type == 'file':
            self.local_path = realpath(self.path)
            self.isdir = isdir(self.local_path)
        else:
            # url, we want to cache it in the local genignore cache
            self.local_path = None

    def load(self):
        if 'file' in self.type:
            with open(self.local_path, 'r') as f:
                namespaced_k = self.local_path_as_key()
                aliased_k = namespaced_k.split('.')[-1]
                self.items[namespaced_k] = f.read()
                self.items[aliased_k] = self.items[namespaced_k]
            assert len(self.items) > 0
        return self

    def local_path_as_key(self):
        return self.path.replace('/', '.')

    def __contains__(self, item):
        return item in self._force_load().items

    def __getitem__(self, key):
        return self._force_load().items[key]

    def _force_load(self):
        if len(self.items) == 0:
            self.load()
        return self


class TemplateSources(object):

    def __init__(self, include_paths):
        self.include_paths = include_paths
        self.sources = []

    def get(self, source):
        pass


class TemplateSource(object):

    def __init__(self, source_path):
        self.source_path = source_path

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