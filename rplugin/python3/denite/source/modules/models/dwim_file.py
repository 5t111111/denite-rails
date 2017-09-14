import re
import os
import inflection

from file_base import FileBase


class DwimFile(FileBase):
    def __init__(self, filepath):
        self.filepath_with_type_info = filepath
        pattern = re.compile(r'^.+: ?')
        self.type_info = re.match(pattern, filepath).group(0)
        self.filepath = re.sub(pattern, '', filepath)

    def remove_base_directory(self, filename, root_path):
        if self.type_info == 'Model: ':
            dirpath = os.path.join(root_path, 'app/models/')
        elif self.type_info == 'Controller: ':
            dirpath = os.path.join(root_path, 'app/controllers/')
        elif self.type_info == 'Helper: ':
            dirpath = os.path.join(root_path, 'app/helpers/')
        elif self.type_info == 'View: ':
            dirpath = os.path.join(root_path, 'app/views/')
        elif self.type_info == 'Test: ':
            dirpath = os.path.join(root_path, 'test/')
        elif self.type_info == 'Spec: ':
            dirpath = os.path.join(root_path, 'spec/')
        return re.sub(dirpath, '', filename)

    def to_word(self, root_path):
        if self.type_info == 'View: ' or self.type_info == 'Test: ' or self.type_info == 'Spec: ':
            return self.remove_base_directory(self.filepath_with_type_info, root_path)
        else:
            return self.to_constant(root_path)

    def to_constant(self, root_path):
        filepath = self.remove_base_directory(self.filename_without_extension(), root_path)
        path_components = filepath.split(os.sep)
        constant = '::'.join(inflection.camelize(path_component) for path_component in path_components)
        return '{0}{1} ({2})'.format(re.search(r'^.+: ?', self.filepath_with_type_info).group(), constant, self.remove_base_directory(self.filepath, root_path))
