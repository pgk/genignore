from os.path import isdir, realpath


class Source(object):

    def __init__(self, path, target=Nones):
        super(Source, self).__init__()

        self.isdir = False
        self.full_path = None
        self.type, self.path = path.split('://')

        assert self.type in ('file', 'http', 'https')

        if self.type == 'file':
            self.full_path = realpath(self.path)
            self.isdir = isdir(self.full_path)
        else:
            pass
        


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