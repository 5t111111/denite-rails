import os
import finder_utils
from view_file import ViewFile


class ViewFinder:
    GLOB_PATTERN = 'app/views/**/*'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        files = [filename for filename in files if os.path.isfile(filename)]
        return [ViewFile(filename) for filename in files]
