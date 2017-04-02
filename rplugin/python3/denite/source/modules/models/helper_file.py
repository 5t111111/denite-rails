import re
import os

from target import Target


class HelperFile(Target):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/helpers/'), '', filename)
