import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath(
        [working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working file_path'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    if not os.path.isfile(target_file):
        result = f'Error: "{file_path}" does not exist or is not a regular file'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    if not target_file.endswith(".py"):
        result = f'Error: "{file_path}" is not a Python file'
        print(
            f"Result for {file_path if file_path != "." else "current"} file_path:\n  {result}")
        return

    command = ["python", target_file]
    if args != None:
        for arg in args:
            command.extend(arg)

    completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

    output_str = ""
    if completed_process.returncode != 0:
        output_str += f"Process exited with code {completed_process.returncode}"

    if len(completed_process.stdout) == 0 and len(completed_process.stderr):
        output_str += "No output produced" 

    output_str += f"STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}"
    print(output_str)