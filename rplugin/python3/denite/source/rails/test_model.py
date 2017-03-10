# -*- coding: utf-8 -*-

import glob
import re

from target import Target

class TestModel(Target):
    def remove_base_directory(self, filename):
        return re.sub(r'^test/', '', filename)

    @staticmethod
    def find_all():
        files = glob.glob('test/**/*.rb', recursive=True)
        return [TestModel(filename) for filename in files]
