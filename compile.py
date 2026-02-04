from utils import compile_directory
import os

if __name__ == "__main__":
    exclude_dirs = ["django_compiler", "env"]
    directory = os.getcwd()
    compile_directory(directory, exclude_dirs=exclude_dirs)