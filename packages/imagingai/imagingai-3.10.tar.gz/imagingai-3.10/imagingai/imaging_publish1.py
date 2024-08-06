import os
import shutil

def prompt_for_directory(prompt_message, default_directory=None):
    """Prompt the user for a directory and return it if valid."""
    while True:
        directory = input(f"{prompt_message} [{default_directory}]: ").strip()
        if not directory and default_directory:
            directory = default_directory
        if os.path.isdir(directory):
            return directory
        else:
            print(f"Directory '{directory}' does not exist. Please try again.")

def main():
    default_source_dir = '/usr/local/extensions'
    source_dir = prompt_for_directory(
        "Please enter the path to the source directory",
        default_directory=default_source_dir
    )

    php_ext_dir = prompt_for_directory(
        "Please enter the path to the PHP extension directory"
    )

    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

    if not os.path.isdir(php_ext_dir):
        raise FileNotFoundError(f"PHP extension directory '{php_ext_dir}' does not exist.")

    so_files = [f for f in os.listdir(source_dir) if f.endswith('.so')]

    for so_file in so_files:
        src_path = os.path.join(source_dir, so_file)
        dest_path = os.path.join(php_ext_dir, so_file)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied {so_file} to {php_ext_dir}")
        else:
            print(f"Source file {src_path} does not exist.")

    print("Extraction completed. Please update php.ini")

if __name__ == "__main__":
    main()
