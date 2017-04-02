import os
import inflection


class FileBase:
    def __init__(self, filepath):
        self.filepath = os.path.normpath(filepath)

    def to_word(self, root_path):
        return self.to_constant(root_path)

    def to_constant(self, root_path):
        filepath = self.remove_base_directory(self.filename_without_extension(), root_path)
        path_components = filepath.split(os.sep)
        constant = '::'.join(inflection.camelize(path_component) for path_component in path_components)
        return '{0} ({1})'.format(constant, self.remove_base_directory(self.filepath, root_path))

    def filename_without_extension(self):
        return os.path.splitext(self.filepath)[0]
