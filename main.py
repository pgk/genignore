import sys
import os
from os import path
import requests
from zipfile import ZipFile
from StringIO import StringIO


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"
GENIGNORE_CACHE = ".genignore_cache"

def init_repo_templates():
	templates = None
	names = dict()

	folder = path.join(path.expanduser("~"), GENIGNORE_CACHE)
	latest_file = path.join(folder, "latest.zip")
	if not path.isdir(folder):
		os.makedirs(folder)
		r = requests.get(MASTER_ARCHIVE, stream=True)
		with open(latest_file, "wb") as f:
			for chunk in r.iter_content(1024):
				f.write(chunk)

	with ZipFile(latest_file, 'r') as latest:
		for zi in latest.infolist():
			name = path.split(zi.filename)[-1].split(".")[0]
			if len(name):
				names[name] = zi.filename
		templates = names.keys()
	return templates, names


def main(args):
	templates, names = init_repo_templates()
	print("exiting")
	return 0


if __name__ == '__main__':
	args = sys.argv[1:]
	exit(main(args))
