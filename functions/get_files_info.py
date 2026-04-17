import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    result = ""
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath(
        [working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        result = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(
            f"Result for {directory if directory != "." else "current"} directory:\n  {result}")
        return
    if not os.path.isdir(target_dir):
        result = f'Error: "{directory}" is not a directory'
        print(
            f"Result for {directory if directory != "." else "current"} directory:\n  {result}")
        return
    for file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file)
        result += f"- {file}: file_size={os.path.getsize(file_path)}bytes, is_dir={os.path.isdir(file_path)} \n"

    print(
        f"Result for {directory if directory != "." else "current"} directory:\n{result}")
