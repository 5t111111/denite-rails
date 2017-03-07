# -*- coding: utf-8 -*-

import glob
import re
import os
import inflection

from target import Target

class Association(Target):
    def __init__(self, filepath):
        self.filepath_with_type_info = filepath
        filepath = re.sub(r'Controller: ', '', filepath)
        filepath = re.sub(r'Model: ', '', filepath)
        filepath = re.sub(r'Helper: ', '', filepath)
        filepath = re.sub(r'View: ', '', filepath)
        filepath = re.sub(r'Test: ', '', filepath)
        self.filepath = os.path.normpath(filepath)

    def remove_base_directory(self, filename):
        filename = re.sub(r'app/models/', '', filename)
        filename = re.sub(r'app/controllers/', '', filename)
        filename = re.sub(r'app/helpers/', '', filename)
        filename = re.sub(r'app/views/', '', filename)
        return filename

    def to_word(self):
        if self.filepath_with_type_info.startswith('View: '):
            return self.remove_base_directory(self.filepath_with_type_info)
        if self.filepath_with_type_info.startswith('Test: '):
            return self.remove_base_directory(self.filepath_with_type_info)
        else:
            return self.to_constant()

    def to_constant(self):
        filepath = self.remove_base_directory(self.filename_without_extension())
        path_components = filepath.split(os.sep)
        constant = '::'.join(inflection.camelize(path_component) for path_component in path_components)
        return '{0}{1} ({2})'.format(re.search(r'^.+: ?', self.filepath_with_type_info).group(), constant, self.remove_base_directory(self.filepath))

    @staticmethod
    def find_associations(context):
        cbname = os.path.normpath(context['__cbname'])
        path = os.path.normpath(context['path'])
        source_name = re.sub(path, '', cbname)
        basename = os.path.basename(source_name)
        basename_without_ext = os.path.splitext(basename)[0]

        if source_name.startswith('/app/models/'):
            pluralized_name = inflection.pluralize(basename_without_ext)

            controller_files = glob.glob('app/controllers/**/*.rb', recursive=True)
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            helper_files = glob.glob('app/helpers/**/*.rb', recursive=True)
            files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

            view_files = glob.glob('app/views/**/*', recursive=True)
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = glob.glob('test/models/**/*.rb', recursive=True)
            files.extend(['Test: {0}'.format(filename) for filename in test_files if pluralized_name in filename or basename_without_ext in filename])

            return [Association(filename) for filename in files]

        if source_name.startswith('/app/controllers/'):
            pluralized_name = re.sub(r'_controller', '', basename_without_ext)
            singularize_name = inflection.singularize(pluralized_name)

            model_files = glob.glob('app/models/**/*.rb', recursive=True)
            files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

            helper_files = glob.glob('app/helpers/**/*.rb', recursive=True)
            files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

            view_files = glob.glob('app/views/**/*', recursive=True)
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = glob.glob('test/controllers/**/*.rb', recursive=True)
            files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

            return [Association(filename) for filename in files]

        if source_name.startswith('/app/helpers/'):
            pluralized_name = re.sub(r'_helper', '', basename_without_ext)
            singularize_name = inflection.singularize(pluralized_name)

            controller_files = glob.glob('app/controllers/**/*.rb', recursive=True)
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            model_files = glob.glob('app/models/**/*.rb', recursive=True)
            files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

            view_files = glob.glob('app/views/**/*', recursive=True)
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = glob.glob('test/controllers/**/*.rb', recursive=True)
            files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

            return [Association(filename) for filename in files]
