import re
import os

from file_base import FileBase


class ControllerFile(FileBase):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/controllers/'), '', filename)
