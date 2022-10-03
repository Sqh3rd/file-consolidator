import os
from Import_Logic import Import_Logic

imp = Import_Logic()

working_dir_name = input("Name of working dir: ")

if not os.path.exists(f"./{working_dir_name}/main.py"):
    print(f"No directory \"{working_dir_name}\" or no file \"main.py\" in \"{working_dir_name}\"")

output_file_name = f"{working_dir_name}_parsed.py"

if not os.path.exists(f"./{output_file_name}"):
    open(f"./{output_file_name}", "w").close()

print(imp.read_imports_from_file(f'{working_dir_name}/main.py'))