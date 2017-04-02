# -*- coding: utf-8 -*-

import glob
import re
import os

import utilities
from target import Target

class View(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/views/'), '', filename)


    def to_word(self, root_path):
        return self.remove_base_directory(self.filepath, root_path)

    @staticmethod
    def find_all(root_path):
        files = utilities.glob_project(root_path, 'app/views/**/*')
        files = [filename for filename in files if os.path.isfile(filename)]
        return [View(filename) for filename in files]
