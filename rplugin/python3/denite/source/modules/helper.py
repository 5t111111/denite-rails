# -*- coding: utf-8 -*-

import glob
import re
import os

import utilities
from target import Target

class Helper(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/helpers/'), '', filename)

    @staticmethod
    def find_all(root_path):
        files = utilities.glob_project(root_path, 'app/helpers/**/*.rb')
        return [Helper(filename) for filename in files]
