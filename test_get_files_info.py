from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

get_files_info("calculator", ".")
get_files_info("calculator", "pkg/calculator.py")
get_files_info("calculator", "/bin")
get_files_info('calculator', "main.py")
