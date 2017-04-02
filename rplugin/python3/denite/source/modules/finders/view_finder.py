import finder_utils

from view_file import ViewFile


class ViewFinder:
    def __init__(self, context):
        self.context = context

    @property
    def root_path(self):
        return self.context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, 'app/views/**/*')
        return [ViewFile(filename) for filename in files]
