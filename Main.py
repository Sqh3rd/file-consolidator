#!/usr/bin/python

import os, argparse
from Import_Logic import Import_Logic
from Logger import Logger

if __name__ == "__main__":
    logger = Logger("Main Logger")
    imp = Import_Logic(logger)

    help_message = "This is a tool to consolidate multiple python files inside a folder to a single python file."

    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument("-i", "--input", help = "Defines the input folder")
    parser.add_argument("-o", "--output", help = "Defines the output file")

    args = parser.parse_args()

    working_dir_name = args.input

    if working_dir_name:
        if not os.path.exists(os.path.join(os.getcwd(), f"{working_dir_name}/main.py")):
            logger.error(f"No directory \"{working_dir_name}\" or no file \"main.py\" in \"{working_dir_name}\"", FileNotFoundError)
    else:
        logger.error(f"No input directory specified!")

    if args.output:
        output_file_name = os.path.join(os.getcwd(), args.output)
    else:
        output_file_name = os.path.join(os.getcwd(), f"{working_dir_name}_parsed.py")

    open(output_file_name, "w").close()

    imp.get_and_cache_imports(os.path.join(working_dir_name, "main.py"), output_file_name)