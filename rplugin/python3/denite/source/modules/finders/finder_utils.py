import glob
import os

def glob_project(root_path, pattern):
    return glob.glob(os.path.join(root_path, pattern), recursive=True)
