import finder_utils

from model_file import ModelFile


class ModelFinder:
    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, 'app/models/**/*.rb')
        return [ModelFile(filename) for filename in files]
