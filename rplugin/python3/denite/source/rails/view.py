# -*- coding: utf-8 -*-

import glob
import re
import os

from target import Target

class View(Target):
    def remove_base_directory(self, filename):
        return re.sub(r'^app/views/', '', filename)

    def to_word(self):
        return self.remove_base_directory(self.filepath)

    @staticmethod
    def find_all():
        files = glob.glob('app/views/**/*', recursive=True)
        files = [filename for filename in files if os.path.isfile(filename)]
        return [View(filename) for filename in files]
