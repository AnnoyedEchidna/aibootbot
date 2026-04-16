import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath(
        [working_dir_abs, target_path]) == working_dir_abs
    if not valid_target_path:
        result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working file_path'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    if os.path.isdir(target_path):
        result = f'Error: Cannot write to "{file_path}" as it is a directory'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w") as f:
        f.write(content)
        f.close()
    
    if os.path.isfile(target_path):
        print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')