import finder_utils

from helper_file import HelperFile


class HelperFinder:

    GLOB_PATTERN = 'app/helpers/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [HelperFile(filename) for filename in files]
