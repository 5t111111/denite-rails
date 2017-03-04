import os

class Target:
    def __init__(self, filepath):
        self.filepath = os.path.normpath(filepath)

    def to_word(self):
        return self.to_constant()

    def to_constant(self):
        filepath = self.remove_base_directory(self.filename_without_extension())
        path_components = filepath.split(os.sep)
        constant = '::'.join(self.to_upper_camel_case(path_component) for path_component in path_components)
        return '{0} ({1})'.format(constant, self.remove_base_directory(self.filepath))

    def filename_without_extension(self):
        return os.path.splitext(self.filepath)[0]

    def to_upper_camel_case(self, snake_case_str):
        components = snake_case_str.split('_')
        return "".join(x.title() for x in components)
