import os

working_dir_name = input("Name of working dir: ")
working_dir = os.fsencode(working_dir_name)

if not os.path.exists(f"./{working_dir_name}/main.py"):
    print(f"No directory \"{working_dir_name}\" or no file \"main.py\" in \"{working_dir_name}\"")

output_file_name = f"{working_dir_name}_parsed.py"

if not os.path.exists(f"./{output_file_name}"):
    open(f"./{output_file_name}", "w").close()

print(imports)