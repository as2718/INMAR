import os
from variables import SOURCE_PATH, OUTPUT_PATH, BAD_OUTPUT_PATH, ARCHIVE_PATH
from module1 import process_file, get_all_files_in_directory
from module2 import export_clean_data


def initialize():
    if not os.path.exists(OUTPUT_PATH) and len(OUTPUT_PATH) != 0:
        os.mkdir(OUTPUT_PATH)

    if not os.path.exists(BAD_OUTPUT_PATH) and len(BAD_OUTPUT_PATH) != 0:
        os.mkdir(BAD_OUTPUT_PATH)

    if not os.path.exists(ARCHIVE_PATH) and len(ARCHIVE_PATH) != 0:
        os.mkdir(ARCHIVE_PATH)

    if len(SOURCE_PATH) != 0 and len(OUTPUT_PATH) != 0 and len(BAD_OUTPUT_PATH) != 0 and len(ARCHIVE_PATH) != 0:
        files_to_process = get_all_files_in_directory(SOURCE_PATH)
        if len(files_to_process) == 0:
            print(f"Source Directory {SOURCE_PATH} is empty, no input files found")
        else:
            for file_path in files_to_process:
                absolute_path = SOURCE_PATH + "/" + file_path
                process_file(absolute_path)
            files_to_process = get_all_files_in_directory(OUTPUT_PATH)
            if len(files_to_process) == 0:
                print(f"Output Directory OUTPUT_PATH is empty, no file validated successfully, "
                      f"look bad files in {BAD_OUTPUT_PATH} ")
            else:
                for file_path in files_to_process:
                    absolute_path = OUTPUT_PATH + "/" + file_path
                    export_clean_data(absolute_path)

    else:
        print(f"SOURCE_PATH, OUTPUT_PATH, BAD_OUTPUT_PATH, ARCHIVE_PATH can not be empty in variables.py file.")


# Main entry point
if __name__ == '__main__':
    initialize()
