from os import path
import shutil
import unittest
import mock
import requests

# from genignore.genignore import parse
# from genignore.genignore import get_cache_paths
# from genignore.genignore import init_repo_templates
#
#
#
#
# def delete_cache():
# 	folder, _ = get_cache_paths()
# 	if path.isdir(folder):
# 		shutil.rmtree(folder)
#
#
# class TestGenignoreParse(unittest.TestCase):
#
# 	def test_assigns_names(self):
# 		args = parse(["gen", "osx", "python", "linux"])
# 		self.assertIsNotNone(args.names)
#
# 	def test_assigns_optionals_if_present(self):
# 		args = parse(["gen", "osx", "python", "linux", "--update"])
# 		self.assertTrue(args.update)
# 		self.assertEquals(args.action, "gen")
#
#
# class TestGenignore_init_repo_templates(unittest.TestCase):
#
# 	@mock.patch('requests.get')
# 	@mock.patch('genignore.genignore.get_templates_from_zipfile')
# 	def test_sync_if_folder_nonexistent(self, mocked_requests_get, mocked_zip):
# 		delete_cache()
# 		init_repo_templates()
# 		self.assertTrue(mocked_requests_get.called)
# 		self.assertTrue(mocked_zip.called)
#
# 	@mock.patch('requests.get')
# 	@mock.patch('genignore.genignore.get_templates_from_zipfile')
# 	def test_sync_if_folder_exists_but_sync_is_True(self, mocked_requests_get, mocked_zip):
# 		init_repo_templates(sync=True)
# 		self.assertTrue(mocked_requests_get.called)
# 		self.assertTrue(mocked_zip.called)


if __name__ == '__main__':
	unittest.main()
