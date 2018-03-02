import finder_utils

from controller_file import ControllerFile


class ControllerFinder:

    GLOB_PATTERN = 'app/controllers/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [ControllerFile(filename) for filename in files]
