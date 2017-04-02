import os
import re

import inflection
import finder_utils

from dwim_file import DwimFile


class DwimFinder:
    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def is_model_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/app/models/')
        return True if base_filepath.startswith(dirpath) else False

    def is_controller_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/app/controllers/')
        return True if base_filepath.startswith(dirpath) else False

    def is_helper_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/app/helpers/')
        return True if base_filepath.startswith(dirpath) else False

    def is_view_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/app/views/')
        return True if base_filepath.startswith(dirpath) else False

    def is_model_test_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/test/models/')
        return True if base_filepath.startswith(dirpath) else False

    def is_controller_test_file(self, base_filepath):
        dirpath = os.path.join(self.root_path, '/test/controllers/')
        return True if base_filepath.startswith(dirpath) else False

    def find_files(self):
        cbname = os.path.normpath(self.context['__cbname'])
        source_name = re.sub(self.root_path, '', cbname)
        basename = os.path.basename(source_name)
        basename_without_ext = os.path.splitext(basename)[0]

        if self.is_model_file(source_name):
            return self._find_dwim_files_for_model(basename_without_ext)
        elif self.is_controller_file(source_name):
            return self._find_dwim_files_for_controller(basename_without_ext)
        elif self.is_helper_file(source_name):
            return self._find_dwim_files_for_helper(basename_without_ext)
        elif self.is_view_file(source_name):
            return self._find_dwim_files_for_view(os.path.dirname(source_name).split('/')[-1])
        elif self.is_model_test_file(source_name):
            return self._find_dwim_files_for_model_test(basename_without_ext)
        elif self.is_controller_test_file(source_name):
            return self._find_dwim_files_for_controller_test(basename_without_ext)

    def _find_dwim_files_for_model(self, base_filename):
        pluralized_name = inflection.pluralize(base_filename)

        controller_files = finder_utils.glob_project(self.root_path, 'app/controllers/**/*.rb')
        files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

        helper_files = finder_utils.glob_project(self.root_path, 'app/helpers/**/*.rb')
        files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

        view_files = finder_utils.glob_project(self.root_path, 'app/views/**/*')
        files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
        test_files = finder_utils.glob_project(self.root_path, 'test/models/**/*.rb')
        files.extend(['Test: {0}'.format(filename) for filename in test_files if pluralized_name in filename or base_filename in filename])

        return [DwimFile(filename) for filename in files]

    def _find_dwim_files_for_controller(self, base_filename):
        pluralized_name = re.sub(r'_controller', '', base_filename)
        singularize_name = inflection.singularize(pluralized_name)

        model_files = finder_utils.glob_project(self.root_path, 'app/models/**/*.rb')
        files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

        helper_files = finder_utils.glob_project(self.root_path, 'app/helpers/**/*.rb')
        files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

        view_files = finder_utils.glob_project(self.root_path, 'app/views/**/*')
        files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
        test_files = finder_utils.glob_project(self.root_path, 'test/controllers/**/*.rb')
        files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

        return [DwimFile(filename) for filename in files]

    def _find_dwim_files_for_helper(self, base_filename):
        pluralized_name = re.sub(r'_helper', '', base_filename)
        singularize_name = inflection.singularize(pluralized_name)

        controller_files = finder_utils.glob_project(self.root_path, 'app/controllers/**/*.rb')
        files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

        model_files = finder_utils.glob_project(self.root_path, 'app/models/**/*.rb')
        files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

        view_files = finder_utils.glob_project(self.root_path, 'app/views/**/*')
        files.extend(['View: {0}'.format(filename) for filename in view_files if os.path.isfile(filename) and pluralized_name in filename])
        test_files = finder_utils.glob_project(self.root_path, 'test/helpers/**/*.rb')
        files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

        return [DwimFile(filename) for filename in files]

    def _find_dwim_files_for_view(self, base_filename):
        pluralized_name = base_filename
        singularize_name = inflection.singularize(pluralized_name)

        controller_files = finder_utils.glob_project(self.root_path, 'app/controllers/**/*.rb')
        files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

        model_files = finder_utils.glob_project(self.root_path, 'app/models/**/*.rb')
        files.extend(['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename])

        helper_files = finder_utils.glob_project(self.root_path, 'app/helpers/**/*.rb')
        files.extend(['Helper: {0}'.format(filename) for filename in helper_files if pluralized_name in filename])

        test_files = finder_utils.glob_project(self.root_path, 'test/controllers/**/*.rb')
        files.extend(['Test: {0}'.format(filename) for filename in test_files if singularize_name in filename or pluralized_name in filename])

        return [DwimFile(filename) for filename in files]

    def _find_dwim_files_for_model_test(self, base_filename):
        singularize_name = re.sub(r'_test', '', base_filename)

        model_files = finder_utils.glob_project(self.root_path, 'app/models/**/*.rb')
        files = ['Model: {0}'.format(filename) for filename in model_files if singularize_name in filename]

        return [DwimFile(filename) for filename in files]

    def _find_dwim_files_for_controller_test(self, base_filename):
        pluralized_name = re.sub(r'_controller_test', '', base_filename)

        controller_files = finder_utils.glob_project(self.root_path, 'app/controllers/**/*.rb')
        files = ['Controller: {0}'.format(filename) for filename in controller_files if pluralized_name in filename]

        return [DwimFile(filename) for filename in files]
