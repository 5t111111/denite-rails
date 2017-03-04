# -*- coding: utf-8 -*-

import glob
import re

from target import Target

class Helper(Target):
    def remove_base_directory(self, filename):
        return re.sub(r'^app/helpers/', '', filename)

    @staticmethod
    def find_all():
        files = glob.glob('app/helpers/**/*.rb', recursive=True)
        return [Helper(filename) for filename in files]
