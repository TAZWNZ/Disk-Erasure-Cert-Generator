import os
import glob
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys

def compile_python_to_so(file_path):
    """
    Compiles a single Python file to a shared object (.so) file.

    :param file_path: The path to the Python file to compile.
    """
    # Prepare the name for the shared object file
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    directory = os.path.dirname(file_path)

    # Change to the directory of the file being compiled
    original_directory = os.getcwd()
    os.chdir(directory)

    # Define an Extension for the Cython module
    ext_modules = [
        Extension(module_name, sources=[file_path])
    ]

    try:
        # Create a setup to build the extension
        setup(
            name=module_name,
            ext_modules=cythonize(ext_modules),
            packages=find_packages(),
            script_args=['build_ext', '--inplace'],  # Build in the current directory
        )

        # Rename the compiled .so file to remove the unwanted suffix
        compiled_files = glob.glob(f"{module_name}*.so")
        for compiled_file in compiled_files:
            new_name = f"{module_name}.so"
            os.rename(compiled_file, new_name)
            print(f"Renamed: {compiled_file} -> {new_name}")

    finally:
        # Change back to the original directory
        os.chdir(original_directory)

    # Return the path to the compiled shared object
    return os.path.join(directory, f"{module_name}.so")

def compile_directory(path, exclude_dirs=None):
    """
    Recursively compiles Python files in a directory while excluding specified directories.

    :param path: The root directory to start searching for Python files.
    :param exclude_dirs: A list of directory names to exclude from compilation.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        # Check if the current directory is in the excluded directories
        if any(exclude_dir in dirpath for exclude_dir in exclude_dirs):
            continue  # Skip excluded directories

        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)

                try:
                    # Compile the Python file to .so
                    compiled_path = compile_python_to_so(file_path)
                    print(f"Compiled: {compiled_path}")

                    # Optionally, delete the original .py file after successful compilation
                    os.remove(file_path)  # Uncomment if you want to delete the original .py file
                except Exception as e:
                    print(f"Error compiling {file_path}: {e}")