import glob
import os
import re


def glob_project(root_path, glob_pattern):
    return glob.glob(os.path.join(root_path, glob_pattern), recursive=True)

def remove_base_directory(filename, root_path, storage):
    return re.sub(os.path.join(root_path, storage), '', filename)
