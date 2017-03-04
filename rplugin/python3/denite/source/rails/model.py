# -*- coding: utf-8 -*-

import glob
import re

from target import Target

class Model(Target):
    def remove_base_directory(self, filename):
        return re.sub(r'^app/models/', '', filename)

    @staticmethod
    def find_all():
        files = glob.glob('app/models/**/*.rb', recursive=True)
        return [Model(filename) for filename in files]
