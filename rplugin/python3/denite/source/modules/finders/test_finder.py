import finder_utils

from test_file import TestFile


class TestFinder:
    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, 'test/**/*.rb')
        return [TestFile(filename) for filename in files]
