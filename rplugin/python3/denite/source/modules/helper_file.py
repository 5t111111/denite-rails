# -*- coding: utf-8 -*-

import re
import os

import utilities
from target import Target

class HelperFile(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/helpers/'), '', filename)

    @staticmethod
    def find_all(context):
        files = utilities.glob_project(context['__root_path'], 'app/helpers/**/*.rb')
        return [HelperFile(filename) for filename in files]
