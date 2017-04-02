# -*- coding: utf-8 -*-

import glob
import re
import os

import utilities
from target import Target

class Controller(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/controllers/'), '', filename)

    @staticmethod
    def find_all(root_path):
        files = utilities.glob_project(root_path, 'app/controllers/**/*.rb')
        return [Controller(filename) for filename in files]
