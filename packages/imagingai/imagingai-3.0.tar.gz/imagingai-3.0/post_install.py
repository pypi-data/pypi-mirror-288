# post_install.py
import os
import shutil
from distutils.sysconfig import get_python_lib

def main():
    # Define the directory where the .so files are located within the package
    package_name = 'imagingai'
    so_files_dir = os.path.join(get_python_lib(), package_name, 'extensions')

    # Define the target directory where you want to copy the .so files
    target_dir = os.path.join('custom', 'folder')

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Copy the .so files to the target directory
    for filename in os.listdir(so_files_dir):
        if filename.endswith('.so'):
            shutil.copy(os.path.join(so_files_dir, filename), target_dir)

    print(f"Copied .so files to {target_dir}")

if __name__ == '__main__':
    main()