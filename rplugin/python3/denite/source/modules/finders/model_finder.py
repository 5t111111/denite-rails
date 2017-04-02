import finder_utils

from model_file import ModelFile


class ModelFinder:

    GLOB_PATTERN = 'app/models/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [ModelFile(filename) for filename in files]
