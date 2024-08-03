import datetime
import json
import logging


def export_to_json(data, file_path):
    """Exports the data to a json file.

    Args:
        data (list[dict]): The data to be exported.
        file_path (str): The path to save the file.
    """
    # check if the file path ends with .json
    if not file_path.endswith(".json"):
        logging.info("Adding .json to the file path...")
        file_path += ".json"  # add .json to the file path

    # write the data to a json file
    with open(file_path, "w") as file:
        logging.info(f"Exporting data to {file_path}...")
        json.dump(data, file, indent=4)
        logging.info("Data exported successfully.")


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


def normalize_data_for_bigquery(data):
    """Normalizes the data for BigQuery by:
    - Replacing periods in the keys with underscores.
    - Replacing the spaces in the keys with underscores.
    - Replacing the slashes in the keys with bars.
    - Replacing the at signs with hashtags.
    - Converting the data to newline delimited json.

    Args:
        data (dict, list[dict]): The data to normalize.

    Returns:
        dict, list[dict]: The normalized data.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    # replace periods, spaces, and slashes in the keys
    data = replace_periods_in_keys(data)
    data = replace_spaces_in_keys(data)
    data = replace_slashes_in_keys(data)

    # convert to newline delimited json
    bq_data = parse_to_nldjson(data, upload_date=False)

    return bq_data


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
        logging.info("Adding upload date and converting data to nldjson...")
        for item in data_to_parse:
            item["upload_date"] = datetime.date.today().isoformat()
            nld_json += f"{json.dumps(item)}\n"

    else:  # upload date is not required
        logging.info("Converting data to nldjson...")
        for item in data_to_parse:
            nld_json += f"{json.dumps(item)}\n"

    return nld_json


def replace_at_sign_in_keys(data):
    """Recursively replaces at signs in the keys of the given data dict or list of dicts with hashtags.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with at signs replaced by underscores in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    # check if the data is valid
    if isinstance(data, dict):
        new_data = {}  # new dictionary to store the data with at signs replaced by underscores
        logging.info("Converting at signs to underscores in dictionary keys...")
        for key, value in data.items():
            new_key = key.replace('@', '#')
            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_at_sign_in_keys(value)
            else:
                new_data[new_key] = value

        logging.info("Dictionary keys converted successfully.")
        return new_data

    elif isinstance(data, list):  # if the data is a list
        new_data = []
        logging.info("Converting at signs to underscores in list of dictionary keys...")
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_at_sign_in_keys(item))
            else:
                new_data.append(item)

        logging.info("List of dictionary keys converted successfully.")
        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


def replace_periods_in_keys(data):
    """Recursively replaces periods in the keys of the given data dict or list of dicts with underscores.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with periods replaced by underscores in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    # check if the data is valid
    if isinstance(data, dict):
        new_data = {}  # new dictionary to store the data with periods replaced by underscores
        logging.info("Converting periods to underscores in dictionary keys...")
        for key, value in data.items():
            new_key = key.replace('.', '_')
            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_periods_in_keys(value)
            else:
                new_data[new_key] = value

        logging.info("Dictionary keys converted successfully.")
        return new_data

    elif isinstance(data, list):  # if the data is a list
        new_data = []
        logging.info("Converting periods to underscores in list of dictionary keys...")
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_periods_in_keys(item))
            else:
                new_data.append(item)

        logging.info("List of dictionary keys converted successfully.")
        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


def replace_slashes_in_keys(data):
    """Recursively replaces slashes in the keys of the given data dict or list of dicts with bars.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with slashes replaced by bars in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    # check if the data is valid
    if isinstance(data, dict):
        new_data = {}  # new dictionary to store the data with slashes replaced by bars
        logging.info("Converting slashes to bars in dictionary keys...")
        for key, value in data.items():
            new_key = key.replace('/', '|')
            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_slashes_in_keys(value)
            else:
                new_data[new_key] = value

        logging.info("Dictionary keys converted successfully.")
        return new_data

    elif isinstance(data, list):  # if the data is a list
        new_data = []
        logging.info("Converting slashes to bars in list of dictionary keys...")
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_slashes_in_keys(item))
            else:
                new_data.append(item)

        logging.info("List of dictionary keys converted successfully.")
        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


def replace_spaces_in_keys(data):
    """Recursively replaces spaces in the keys of the given data dict or list of dicts with underscores.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with spaces replaced by underscores in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    # check if the data is valid
    if isinstance(data, dict):
        new_data = {}  # new dictionary to store the data with spaces replaced by underscores
        logging.info("Converting spaces to underscores in dictionary keys...")
        for key, value in data.items():
            new_key = key.replace(' ', '_')
            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_spaces_in_keys(value)
            else:
                new_data[new_key] = value

        logging.info("Dictionary keys converted successfully.")
        return new_data

    elif isinstance(data, list):  # if the data is a list
        new_data = []
        logging.info("Converting spaces to underscores in list of dictionary keys...")
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_spaces_in_keys(item))
            else:
                new_data.append(item)

        logging.info("List of dictionary keys converted successfully.")
        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")
