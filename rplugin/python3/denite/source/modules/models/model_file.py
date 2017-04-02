import re
import os

from target import Target


class ModelFile(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/models/'), '', filename)
