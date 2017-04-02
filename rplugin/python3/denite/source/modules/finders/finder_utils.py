import glob
import os


def glob_project(root_path, glob_pattern):
    return glob.glob(os.path.join(root_path, glob_pattern), recursive=True)
