import os
from inflector import Inflector

class Target:
    def __init__(self, filepath):
        self.filepath = os.path.normpath(filepath)

    def to_word(self):
        return self.to_constant()

    def to_constant(self):
        filepath = self.remove_base_directory(self.filename_without_extension())
        path_components = filepath.split(os.sep)
        constant = '::'.join(Inflector().camelize(path_component) for path_component in path_components)
        return '{0} ({1})'.format(constant, self.remove_base_directory(self.filepath))

    def filename_without_extension(self):
        return os.path.splitext(self.filepath)[0]
