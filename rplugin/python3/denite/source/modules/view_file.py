# -*- coding: utf-8 -*-

import re
import os

import utilities
from target import Target

class ViewFile(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/views/'), '', filename)


    def to_word(self, root_path):
        return self.remove_base_directory(self.filepath, root_path)

    @staticmethod
    def find_all(context):
        files = utilities.glob_project(context['__root_path'], 'app/views/**/*')
        files = [filename for filename in files if os.path.isfile(filename)]
        return [ViewFile(filename) for filename in files]
