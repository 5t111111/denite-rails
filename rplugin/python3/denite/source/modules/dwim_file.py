# -*- coding: utf-8 -*-

import re
import os
import inflection

import utilities
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

    @staticmethod
    def find_associations(context):
        root_path = context['__root_path']
        cbname = os.path.normpath(context['__cbname'])
        source_name = re.sub(root_path, '', cbname)
        basename = os.path.basename(source_name)
        basename_without_ext = os.path.splitext(basename)[0]

        if source_name.startswith(os.path.join(root_path, '/app/models/')):
            pluralized_name = inflection.pluralize(basename_without_ext)

            controller_files = utilities.glob_project(root_path, 'app/controllers/**/*.rb')
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            helper_files = utilities.glob_project(root_path, 'app/helpers/**/*.rb')
            files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

            view_files = utilities.glob_project(root_path, 'app/views/**/*')
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = utilities.glob_project(root_path, 'test/models/**/*.rb')
            files.extend(['Test: {0}'.format(filename) for filename in test_files if pluralized_name in filename or basename_without_ext in filename])

            return [DwimFile(filename) for filename in files]

        if source_name.startswith(os.path.join(root_path, '/app/controllers/')):
            pluralized_name = re.sub(r'_controller', '', basename_without_ext)
            singularize_name = inflection.singularize(pluralized_name)

            model_files = utilities.glob_project(root_path, 'app/models/**/*.rb')
            files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

            helper_files = utilities.glob_project(root_path, 'app/helpers/**/*.rb')
            files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

            view_files = utilities.glob_project(root_path, 'app/views/**/*')
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = utilities.glob_project(root_path, 'test/controllers/**/*.rb')
            files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

            return [DwimFile(filename) for filename in files]

        if source_name.startswith(os.path.join(root_path, '/app/helpers/')):
            pluralized_name = re.sub(r'_helper', '', basename_without_ext)
            singularize_name = inflection.singularize(pluralized_name)

            controller_files = utilities.glob_project(root_path, 'app/controllers/**/*.rb')
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            model_files = utilities.glob_project(root_path, 'app/models/**/*.rb')
            files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

            view_files = utilities.glob_project(root_path, 'app/views/**/*')
            files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
            test_files = utilities.glob_project(root_path, 'test/helpers/**/*.rb')
            files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

            return [DwimFile(filename) for filename in files]

        if source_name.startswith(os.path.join(root_path, '/app/views/')):
            pluralized_name = os.path.dirname(source_name).split('/')[-1]
            singularize_name = inflection.singularize(pluralized_name)

            controller_files = utilities.glob_project(root_path, 'app/controllers/**/*.rb')
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            model_files = utilities.glob_project(root_path, 'app/models/**/*.rb')
            files.extend(['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename])

            helper_files = utilities.glob_project(root_path, 'app/helpers/**/*.rb')
            files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

            test_files = utilities.glob_project(root_path, 'test/controllers/**/*.rb')
            files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

            return [DwimFile(filename) for filename in files]

        if source_name.startswith(os.path.join(root_path, '/test/models/')):
            singularize_name = re.sub(r'_test', '', basename_without_ext)

            model_files = utilities.glob_project(root_path, 'app/models/**/*.rb')
            files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

            return [DwimFile(filename) for filename in files]

        if source_name.startswith(os.path.join(root_path, '/test/controllers/')):
            pluralized_name = re.sub(r'_controller_test', '', basename_without_ext)

            controller_files = utilities.glob_project(root_path, 'app/controllers/**/*.rb')
            files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

            return [DwimFile(filename) for filename in files]
