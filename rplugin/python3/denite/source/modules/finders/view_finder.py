import finder_utils

from view_file import ViewFile


class ViewFinder:
    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, 'app/views/**/*')
        return [ViewFile(filename) for filename in files]
