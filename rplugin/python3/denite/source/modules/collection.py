import glob
import os

from dwim_finder import DwimFinder
from model_finder import ModelFinder
from controller_finder import ControllerFinder
from helper_finder import HelperFinder
from view_finder import ViewFinder
from test_finder import TestFinder


class Collection:
    def __init__(self, context):
        self.context = context

    def find_files(self):
        if self.context['__target'] == 'dwim':
            return DwimFinder(self.context).find_files()
        elif self.context['__target'] == 'model':
            return ModelFinder(self.context).find_files()
        elif self.context['__target'] == 'controller':
            return ControllerFinder(self.context).find_files()
        elif self.context['__target'] == 'helper':
            return HelperFinder(self.context).find_files()
        elif self.context['__target'] == 'view':
            return ViewFinder(self.context).find_files()
        elif self.context['__target'] == 'test':
            return TestFinder(self.context).find_files()
        else:
            raise NameError('{0} is not valid denite-rails target'.format(
                self.context['__target']))

    def root_path(self):
        return self.context['__root_path']

    def _glob_project(self, pattern):
        return glob.glob(os.path.join(self.context['__root_path'], pattern), recursive=True)
