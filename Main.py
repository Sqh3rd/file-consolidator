#!/usr/bin/python

import os, argparse
from Error_Object import Error_Object
from Import_Logic import Import_Logic
from Log_Mode import Log_Mode
from Log_Mode_Parser import Log_Mode_Parser
from Logger import Logger
from Output import Output

if __name__ == "__main__":
    help_message = "This is a tool to consolidate multiple python files inside a folder to a single python file."

    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument("-i", "--input", help = "Defines the input folder")
    parser.add_argument("-o", "--output", help = "Defines the output file")
    parser.add_argument("-lm", "--log_mode", help = f"Log mode determines what messages get logged. Log Modes are: {', '.join([i.name.lower() for i in Log_Mode])}")

    args = parser.parse_args()

    log_mode = Log_Mode.STANDARD
    if args.log_mode:
        log_mode = Log_Mode_Parser().parse_str(args.log_mode)

    logger = Logger("Main Logger", Output.STDOUT, log_mode)

    working_dir_name = args.input

    if working_dir_name:
        if not os.path.exists(os.path.join(os.getcwd(), f"{working_dir_name}/main.py")):
            error_obj = Error_Object(f"No directory \"{working_dir_name}\" or no file \"main.py\" in \"{working_dir_name}\"", FileNotFoundError)
            logger.error(error_obj)
    else:
        error_obj = Error_Object(f"No input directory specified!", argparse.ArgumentError)
        logger.error(error_obj)

    if args.output:
        output_file_name = os.path.join(os.getcwd(), args.output)
    else:
        output_file_name = os.path.join(os.getcwd(), f"{working_dir_name}_consolidated.py")

    open(output_file_name, "w").close()

    imp = Import_Logic(logger)

    imp.get_and_cache_imports(os.path.join(working_dir_name, "main.py"), output_file_name)