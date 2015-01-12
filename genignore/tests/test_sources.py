#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from genignore import sources


class SourceTest(unittest.TestCase):

	def test_exists(self):
		source = sources.Source(path='file://genignore/tests/data/example')
		self.assertEquals(source.path, 'genignore/tests/data/example')
		self.assertEquals(source.type, 'file')

	def test_throw_if_not_http_or_file(self):
		self.assertRaises(AssertionError, sources.Source, path='blob://foo.txt')

	def test_behaves_as_dict(self):
		source = sources.Source(path='file://genignore/tests/data/example')
		self.assertTrue('genignore.tests.data.example' in source)

	def test_aliases_to_example(self):
		source = sources.Source(path='file://genignore/tests/data/example')
		self.assertTrue('example' in source)

	def test_key_access(self):
		source = sources.Source(path='file://genignore/tests/data/example')
		self.assertTrue('.example' in source['example'])