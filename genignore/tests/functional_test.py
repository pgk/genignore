#!/usr/bin/env python
# -*- coding: utf-8 -*-

from genignore.tests import test_helpers as ft
from os import path
from contextlib import contextmanager

inform = ft.log.info
shell = ft.shell
check_exists = ft.check_exists
log = ft.log


HOME = path.expanduser('~')
PWD = path.dirname(path.realpath(__file__))
ROOT = path.realpath(path.join(PWD, './../../'))
CACHE = path.join(HOME, '.genignore_cache')
LATEST = path.join(CACHE, 'latest.zip')
TEST_IGNORE = path.join(ROOT, 'test_ignore')


rm_ignore = lambda : shell('rm %s' % TEST_IGNORE)

def assert_exists(file_or_dir):
	assert check_exists(file_or_dir) == True, "FAIL: %s should exist" % file_or_dir


def do_cleanup():
	inform('setting up')
	inform('removing %s' % CACHE)

	shell('rm -rf %s/*.*' % CACHE)
	shell('rm -rf .venv')
	rm_ignore()

def set_venv_and_install_genignore():
	shell('virtualenv --no-site-packages .venv')
	shell('.venv/bin/python setup.py develop')


@contextmanager
def test_context(setup=None, teardown=None):
	do_cleanup()
	try:
		if callable(setup):
			setup()
		yield
	finally:
		try:
			if callable(teardown):
			teardown()
		except Exception, e:
			print(e)

		do_cleanup()


with test_context():

	shell('virtualenv --no-site-packages .venv')
	shell('.venv/bin/python setup.py develop')


	# TEST SYNC

	shell('.venv/bin/genignore sync', preserve_output=True)
	assert_exists(LATEST)
	inform('SUCCESS!')

	# TEST SYNC

	r = shell('.venv/bin/genignore list', preserve_output=True)
	inform(str(r[0]))
	inform('SUCCESS!')

	# TEST GEN

	shell('genignore gen osx --out=%s' % TEST_IGNORE, preserve_output=True)
	assert_exists(TEST_IGNORE)
	inform('SUCCESS!')
	rm_ignore()

	# TEST ADD

	shell('genignore gen osx --out=%s' % TEST_IGNORE, preserve_output=True)
	assert_exists(TEST_IGNORE)

	shell('genignore gen linux --out=%s --add' % TEST_IGNORE, preserve_output=True)
	assert_exists(TEST_IGNORE)
	inform('SUCCESS!')
	rm_ignore()

	# run bash -c "cat .test_ignore | grep genignore"
	# rm -f .test_ignore

	# res = shell('genignore gen osx jetbrains linux python | grep <genignore')
	# print(res)

	# deactivate
	# rm .test_ignore
	# # echo removing $HOME/.genignore_cache
	# # rm -rf $HOME/.genignore_cache/*.*

	# # echo removing .venv
	# # rm -rf .venv











