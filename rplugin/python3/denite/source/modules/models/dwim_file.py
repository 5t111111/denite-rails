import re
import os
import inflection

from target import Target


class DwimFile(Target):
    def __init__(self, filepath):
        self.filepath_with_type_info = filepath
        filepath = re.sub(r'Controller: ', '', filepath)
        filepath = re.sub(r'Model: ', '', filepath)
        filepath = re.sub(r'Helper: ', '', filepath)
        filepath = re.sub(r'View: ', '', filepath)
        filepath = re.sub(r'Test: ', '', filepath)
        self.filepath = os.path.normpath(filepath)

    def remove_base_directory(self, filename, root_path):
        filename = re.sub(os.path.join(root_path, 'app/models/'), '', filename)
        filename = re.sub(os.path.join(root_path, 'app/controllers/'), '', filename)
        filename = re.sub(os.path.join(root_path, 'app/helpers/'), '', filename)
        filename = re.sub(os.path.join(root_path, 'app/views/'), '', filename)
        filename = re.sub(os.path.join(root_path, 'test/'), '', filename)
        return filename

    def to_word(self, root_path):
        if self.filepath_with_type_info.startswith('View: '):
            return self.remove_base_directory(self.filepath_with_type_info, root_path)
        if self.filepath_with_type_info.startswith('Test: '):
            return self.remove_base_directory(self.filepath_with_type_info, root_path)
        else:
            return self.to_constant(root_path)

    def to_constant(self, root_path):
        filepath = self.remove_base_directory(self.filename_without_extension(), root_path)
        path_components = filepath.split(os.sep)
        constant = '::'.join(inflection.camelize(path_component) for path_component in path_components)
        return '{0}{1} ({2})'.format(re.search(r'^.+: ?', self.filepath_with_type_info).group(), constant, self.remove_base_directory(self.filepath, root_path))
