# File write and trim operations

import os
import logging.config
from typing import List


class FileHandler:
    @staticmethod
    def add_project_path(relative_file_path: str) -> str:
        return os.path.abspath(f'{relative_file_path}')

    @staticmethod
    def clear_file(logger: logging.Logger, file_path: str) -> None:
        try:
            open(file_path, 'w').close()
        except FileNotFoundError as file_not_found:
            logger.error(f'Found no file to clear: {file_not_found}')
        except Exception as e:
            logger.exception(f'Exception was thrown', e)

    @staticmethod
    def file_exists(relative_file_path: str) -> bool:
        return os.path.exists(relative_file_path)

    @staticmethod
    def append_line_to_file(logger: logging.Logger, data: str, file_path: str) -> None:
        try:
            with open(file_path, 'a') as liveData:
                liveData.write('%s\n' % data)
            file_name: str = file_path.rsplit("/", 1)[1]
            logger.info(f'Inserting line to {file_name}')
        except FileNotFoundError as file_not_found:
            logger.error(f'Found no file to append to: {file_not_found}')
        except Exception as e:
            logger.exception(f'Exception was thrown', e)

    @staticmethod
    def trim_data(logger: logging.Logger, data_file_path: str, num_to_trim_to: int) -> None:
        # check if data file has reach the configured live data limit
        logger.debug('trim data running')
        try:
            with open(data_file_path, 'r') as data:
                num_lines: int = sum(1 for line in data)

            if num_lines - 1 > num_to_trim_to:
                with open(data_file_path, 'r') as infile:
                    lines: List[str] = infile.readlines()

                with open(data_file_path, 'w') as outfile:
                    for pos, line in enumerate(lines):
                        if pos != 1:
                            outfile.write(line)
        except FileNotFoundError as file_not_found:
            logger.error(f'Trim_data found no file to trim: {file_not_found}')
            exit()
        except Exception as e:
            logger.exception(f'Exception was thrown', e)
