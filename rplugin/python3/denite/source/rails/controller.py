# -*- coding: utf-8 -*-

import glob
import re

from target import Target

class Controller(Target):
    def remove_base_directory(self, filename):
        return re.sub(r'^app/controllers/', '', filename)

    @staticmethod
    def find_all():
        files = glob.glob('app/controllers/**/*.rb', recursive=True)
        return [Controller(filename) for filename in files]
