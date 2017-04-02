# -*- coding: utf-8 -*-

import re
import os

import utilities
from target import Target

class ControllerFile(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/controllers/'), '', filename)
