import os
from Import_Logic import Import_Logic
from Logger import Logger

logger = Logger("Main Logger")
imp = Import_Logic(logger)

working_dir_name = input("Name of working dir: ")

if not os.path.exists(f"./{working_dir_name}/main.py"):
    logger.error(f"No directory \"{working_dir_name}\" or no file \"main.py\" in \"{working_dir_name}\"", FileNotFoundError)

output_file_name = f"{working_dir_name}_parsed.py"

open(f"./{output_file_name}", "w").close()

imp.get_and_cache_imports(f"{working_dir_name}/main.py", output_file_name)