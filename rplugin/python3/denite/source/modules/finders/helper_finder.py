import finder_utils

from helper_file import HelperFile


class HelperFinder:
    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, 'app/helpers/**/*.rb')
        return [HelperFile(filename) for filename in files]
