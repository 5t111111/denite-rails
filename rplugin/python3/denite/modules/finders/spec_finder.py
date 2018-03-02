import finder_utils

from spec_file import SpecFile


class SpecFinder:

    GLOB_PATTERN = 'spec/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [SpecFile(filename) for filename in files]
