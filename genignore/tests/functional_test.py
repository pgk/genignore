#!/usr/bin/env python
# -*- coding: utf-8 -*-

from genignore.tests import test_helpers as ft
from os import path


inform = ft.log.info
shell = ft.shell
check_exists = ft.check_exists


HOME = path.expanduser('~')


CACHE = path.join(HOME, '.genignore_cache')
LATEST = path.join(CACHE, 'latest.zip')
TEST_IGNORE = 'test_ignore'


def do_cleanup():
	inform('setting up')
	inform('removing %s' % CACHE)

	shell('rm -rf %s/*.*' % CACHE)
	shell('rm -rf .venv')
	shell('rm -f %s' % TEST_IGNORE)


do_cleanup()
shell('virtualenv --no-site-packages .venv')
shell('.venv/bin/python setup.py develop')


# TEST SYNC

shell('.venv/bin/genignore sync')
assert check_exists(LATEST) == True, "FAIL: %s should have been created" % LATEST
inform('SUCCESS!')


# TEST GEN

shell('genignore gen osx --out=%s' % TEST_IGNORE)
assert check_exists(TEST_IGNORE) == True, "FAIL: %s should exist" % TEST_IGNORE
inform('SUCCESS!')
shell('rm -f .test_ignore')


shell('genignore gen osx --out=%s --add linux' % TEST_IGNORE)
assert check_exists(TEST_IGNORE) == True, "FAIL: %s should exist" % TEST_IGNORE
inform('SUCCESS!')
shell('rm -f .test_ignore')

# run bash -c "cat .test_ignore | grep genignore"
# rm -f .test_ignore

res = shell('genignore gen osx jetbrains linux python | grep <genignore')
print(res)

# deactivate
# rm .test_ignore
# # echo removing $HOME/.genignore_cache
# # rm -rf $HOME/.genignore_cache/*.*

# # echo removing .venv
# # rm -rf .venv
do_cleanup()










