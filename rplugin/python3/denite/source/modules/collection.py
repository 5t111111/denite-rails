from dwim_file import DwimFile
from model_file import ModelFile
from controller_file import ControllerFile
from helper_file import HelperFile
from test_file import TestFile
from view_file import ViewFile


class Collection:
    def __init__(self, context):
        self.context = context

    def find_files(self):
        if self.context['__target'] == 'dwim':
            return DwimFile.find_associations(self.context)
        elif self.context['__target'] == 'model':
            return ModelFile.find_all(self.context)
        elif self.context['__target'] == 'controller':
            return ControllerFile.find_all(self.context)
        elif self.context['__target'] == 'view':
            return ViewFile.find_all(self.context)
        elif self.context['__target'] == 'helper':
            return HelperFile.find_all(self.context)
        elif self.context['__target'] == 'test':
            TestFile.find_all(self.context)
        else:
            raise NameError('{0} is not valid denite-rails target'.format(
                self.context['__target']
                ))
