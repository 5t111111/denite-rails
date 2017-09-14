import os
import re

import inflection
import finder_utils

from dwim_file import DwimFile


class DwimFinder:

    MODEL_GLOB_PATTERN = 'app/models/**/*.rb'
    CONTROLLER_GLOB_PATTERN = 'app/controllers/**/*.rb'
    HELPER_GLOB_PATTERN = 'app/helpers/**/*.rb'
    VIEW_GLOB_PATTERN = 'app/views/**/*'
    MODEL_TEST_GLOB_PATTERN = 'test/models/**/*.rb'
    CONTROLLER_TEST_GLOB_PATTERN = 'test/controllers/**/*.rb'
    HELPER_TEST_GLOB_PATTERN = 'test/helpers/**/*.rb'
    MODEL_SPEC_GLOB_PATTERN = 'spec/models/**/*.rb'
    CONTROLLER_SPEC_GLOB_PATTERN = 'spec/controllers/**/*.rb'
    HELPER_SPEC_GLOB_PATTERN = 'spec/helpers/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']
        cbname = os.path.normpath(self.context['__cbname'])
        self.source_path = re.sub(self.root_path, '', cbname)

    @property
    def source_name(self):
        basename = os.path.basename(self.source_path)

        if self._is_controller_file():
            basename = re.sub(r'_controller', '', basename)
        elif self._is_helper_file():
            basename = re.sub(r'_helper', '', basename)
        elif self._is_view_file():
            basename = os.path.dirname(self.source_path).split('/')[-1]
        elif self._is_model_test_file():
            basename = re.sub(r'_test', '', basename)
        elif self._is_controller_test_file():
            basename = re.sub(r'_controller_test', '', basename)
        elif self._is_model_spec_files():
            basename = re.sub(r'_spec', '', basename)
        elif self._is_controller_spec_files():
            basename = re.sub(r'_controller_spec', '', basename)

        return os.path.splitext(basename)[0]

    @property
    def pluralized_name(self):
        return inflection.pluralize(self.source_name)

    @property
    def singularized_name(self):
        return inflection.singularize(self.source_name)

    def find_files(self):
        if self._is_model_file():
            return self._find_dwim_files_for_model()
        elif self._is_controller_file():
            return self._find_dwim_files_for_controller()
        elif self._is_helper_file():
            return self._find_dwim_files_for_helper()
        elif self._is_view_file():
            return self._find_dwim_files_for_view()
        elif self._is_model_test_file():
            return self._find_dwim_files_for_model_test()
        elif self._is_controller_test_file():
            return self._find_dwim_files_for_controller_test()
        elif self._is_model_spec_files():
            return self._find_dwim_files_for_model_spec()
        elif self._is_controller_spec_files():
            return self._find_dwim_files_for_controller_spec()

    def _find_dwim_files_for_model(self):
        result_list = []
        result_list.extend(self._create_controller_list())
        result_list.extend(self._create_helper_list())
        result_list.extend(self._create_view_list())
        result_list.extend(self._create_model_test_list())
        result_list.extend(self._create_model_spec_list())
        return [DwimFile(x) for x in result_list]

    def _find_dwim_files_for_controller(self):
        result_list = []
        result_list.extend(self._create_model_list())
        result_list.extend(self._create_helper_list())
        result_list.extend(self._create_view_list())
        result_list.extend(self._create_controller_test_list())
        result_list.extend(self._create_controller_spec_list())
        return [DwimFile(x) for x in result_list]

    def _find_dwim_files_for_helper(self):
        result_list = []
        result_list.extend(self._create_controller_list())
        result_list.extend(self._create_model_list())
        result_list.extend(self._create_view_list())
        result_list.extend(self._create_helper_test_list())
        result_list.extend(self._create_helper_spec_list())
        return [DwimFile(x) for x in result_list]

    def _find_dwim_files_for_view(self):
        result_list = []
        result_list.extend(self._create_controller_list())
        result_list.extend(self._create_model_list())
        result_list.extend(self._create_helper_list())
        result_list.extend(self._create_helper_spec_list())
        return [DwimFile(filename) for filename in result_list]

    def _find_dwim_files_for_model_test(self):
        result_list = []
        result_list.extend(self._create_model_list())
        return [DwimFile(filename) for filename in result_list]

    def _find_dwim_files_for_controller_test(self):
        result_list = []
        result_list.extend(self._create_controller_list())
        return [DwimFile(filename) for filename in result_list]

    def _find_dwim_files_for_model_spec(self):
        result_list = []
        result_list.extend(self._create_model_list())
        return [DwimFile(filename) for filename in result_list]

    def _find_dwim_files_for_controller_spec(self):
        result_list = []
        result_list.extend(self._create_controller_list())
        return [DwimFile(filename) for filename in result_list]

    def _is_model_file(self):
        dirpath = os.path.join(self.root_path, '/app/models/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_controller_file(self):
        dirpath = os.path.join(self.root_path, '/app/controllers/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_helper_file(self):
        dirpath = os.path.join(self.root_path, '/app/helpers/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_view_file(self):
        dirpath = os.path.join(self.root_path, '/app/views/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_model_test_file(self):
        dirpath = os.path.join(self.root_path, '/test/models/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_controller_test_file(self):
        dirpath = os.path.join(self.root_path, '/test/controllers/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_helper_test_file(self):
        dirpath = os.path.join(self.root_path, '/test/helpers/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_model_spec_files(self):
        dirpath = os.path.join(self.root_path, '/spec/models/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_controller_spec_files(self):
        dirpath = os.path.join(self.root_path, '/spec/controllers/')
        return True if self.source_path.startswith(dirpath) else False

    def _is_helper_spec_files(self):
        dirpath = os.path.join(self.root_path, '/spec/helpers/')
        return True if self.source_path.startswith(dirpath) else False

    def _create_model_list(self):
        l = self._find_model_files()
        return ['Model: {0}'.format(x) for x in l]

    def _create_controller_list(self):
        l = self._find_controller_files()
        return ['Controller: {0}'.format(x) for x in l]

    def _create_helper_list(self):
        l = self._find_helper_files()
        return ['Helper: {0}'.format(x) for x in l]

    def _create_view_list(self):
        l = self._find_view_files()
        return ['View: {0}'.format(x) for x in l]

    def _create_model_test_list(self):
        l = self._find_model_test_files()
        return ['Test: {0}'.format(x) for x in l]

    def _create_controller_test_list(self):
        l = self._find_controller_test_files()
        return ['Test: {0}'.format(x) for x in l]

    def _create_helper_test_list(self):
        l = self._find_helper_test_files()
        return ['Test: {0}'.format(x) for x in l]

    def _create_model_spec_list(self):
        l = self._find_model_spec_files()
        return ['Spec: {0}'.format(x) for x in l]

    def _create_controller_spec_list(self):
        l = self._find_controller_spec_files()
        return ['Spec: {0}'.format(x) for x in l]

    def _create_helper_spec_list(self):
        l = self._find_helper_spec_files()
        return ['Spec: {0}'.format(x) for x in l]

    def _find_model_files(self):
        l = finder_utils.glob_project(self.root_path, self.MODEL_GLOB_PATTERN)
        return [x for x in l if self.singularized_name in x]

    def _find_controller_files(self):
        l = finder_utils.glob_project(self.root_path,
                                      self.CONTROLLER_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x]

    def _find_helper_files(self):
        l = finder_utils.glob_project(self.root_path, self.HELPER_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x]

    def _find_view_files(self):
        l = finder_utils.glob_project(self.root_path, self.VIEW_GLOB_PATTERN)
        return [x for x in l if os.path.isfile(x) and self.pluralized_name in x]

    def _find_model_test_files(self):
        l = finder_utils.glob_project(self.root_path, self.MODEL_TEST_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]

    def _find_controller_test_files(self):
        l = finder_utils.glob_project(self.root_path, self.CONTROLLER_TEST_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]

    def _find_helper_test_files(self):
        l = finder_utils.glob_project(self.root_path, self.HELPER_TEST_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]

    def _find_model_spec_files(self):
        l = finder_utils.glob_project(self.root_path, self.MODEL_SPEC_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]

    def _find_controller_spec_files(self):
        l = finder_utils.glob_project(self.root_path, self.CONTROLLER_SPEC_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]

    def _find_helper_spec_files(self):
        l = finder_utils.glob_project(self.root_path, self.HELPER_SPEC_GLOB_PATTERN)
        return [x for x in l if self.pluralized_name in x or self.singularized_name in x]
