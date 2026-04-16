import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath(
        [working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        result = f'Error: Cannot read "{file_path}" as it is outside the permitted working file_path'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    if not os.path.isfile(target_file):
        result = f'Error: File not found or is not a regular file: "{file_path}"'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    with open(target_file, "r") as f:
        file_content_str = f.read(MAX_CHARS)
        if f.read(1):
            file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        print(file_content_str)
        f.close()
        