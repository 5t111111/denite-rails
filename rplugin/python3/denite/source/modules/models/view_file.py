import re
import os

from file_base import FileBase


class ViewFile(FileBase):
    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, 'app/views/'), '', filename)

    def to_word(self, root_path):
        return self.remove_base_directory(self.filepath, root_path)
