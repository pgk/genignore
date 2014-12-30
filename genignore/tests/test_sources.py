#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from genignore import sources


class SourceTest(unittest.TestCase):

	def test_exists(self):
		source = sources.Source(path='file://data/example')
		self.assertEquals(source.path, 'data/example')
		self.assertEquals(source.type, 'file')

	def test_throw_if_not_http_or_file(self):
		self.assertRaises(AssertionError, sources.Source, path='blob://foo.txt')