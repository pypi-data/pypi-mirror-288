import datetime
import json
import logging


def export_list_of_dicts_to_file(data, file_path):
    """Exports the data to a file.

    Args:
        data (list[dict]): The data to be exported.
        file_path (str): The path to save the file.
    """
    with open(file_path, "w") as file:
        for item in data:
            file.write(f"{json.dumps(item)}\n")


def initialize_logger(file_handler_path=None):
    """Initializes a logger with a stream handler and an optional file handler.

    Args:
        file_handler_path (str, optional): The path to save the log file if a file handler is desired. Defaults to None.
    """
    # set up logger
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    logger = logging.getLogger()  # root logger

    # check if there's any handlers already
    if not logger.handlers:
        # create file handler if path is provided
        if file_handler_path:
            # check if the path ends with a slash
            if file_handler_path.endswith('/'):
                file_handler = logging.FileHandler(f"{file_handler_path}{today}.log")
            else:
                file_handler = logging.FileHandler(f"{file_handler_path}/{today}.log")
            # set level to DEBUG
            file_handler.setLevel(logging.DEBUG)
            # set format
            file_handler.setFormatter(logging.Formatter(
                "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
            # add file handler to the logger
            logger.addHandler(file_handler)

        # Create stream handler and set level to ERROR
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(
            "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
        # add stream handler to the logger
        logger.addHandler(stream_handler)

    # Set the logger's level to the lowest level among all handlers
    logger.setLevel(logging.DEBUG)

    return logger


def parse_to_nldjson(data_to_parse, upload_date=True):
    """Parses the given data into newline delimited json.
    Adds the upload date to the payload and ensures the columns do not have invalid characters.

    Args:
        data_to_parse (dict, list[dict]): The data to be parsed.
        upload_date (bool, optional): Whether to add the upload date to the payload. Defaults to True.

    Returns:
        str: The newline delimited json.
    """
    # check if the data is valid
    if isinstance(data_to_parse, str):
        raise TypeError("Data to parse must be a dictionary or a list of dictionaries.")

    # string to store nldjson
    nld_json = ""

    # convert dict to list if there's only one item
    if isinstance(data_to_parse, dict):
        data_to_parse = [data_to_parse]

    # convert to newline delimited json
    if upload_date:  # add upload date to the payload
        for item in data_to_parse:
            item["upload_date"] = datetime.date.today().isoformat()
            nld_json += f"{json.dumps(item)}\n"

    else:  # upload date is not required
        for item in data_to_parse:
            nld_json += f"{json.dumps(item)}\n"

    return nld_json
