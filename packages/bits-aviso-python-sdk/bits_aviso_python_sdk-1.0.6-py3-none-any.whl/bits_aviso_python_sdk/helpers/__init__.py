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


# def fix_invalid_keys(data):
#     """Fixes invalid keys in the data by:
#         - Replacing periods in the keys with underscores.
#         - Replacing the spaces in the keys with underscores.
#         - Replacing the slashes in the keys with bars.
#         - Replacing the at signs with hashtags.
#
#     Args:
#         data (dict, list[dict]): The data to fix the keys for.
#
#     Returns:
#         dict, list[dict]: The data with the invalid keys replaced.
#
#     Raises:
#         TypeError: If the data is not a dictionary or a list of dictionaries.
#     """
    # # replace periods, spaces, and slashes in the keys
    # if isinstance(data, dict):
    #     clean_data = {}  # new dictionary to store the data with at signs replaced by underscores
    #     for key, value in data.items():
    #         if not key:  # if the key is empty, replace it with an underscore
    #             key = '_'
    #         if '@' in key:  # if the key has an at sign, replace it with a hashtag
    #             key = key.replace('@', '#')
    #         if '.' in key:  # if the key has a period, replace it with an underscore
    #             key = key.replace('.', '_')
    #         if ' ' in key:
    #             key = key.replace(' ', '_')
    #         if '/' in key:
    #             key = key.replace('/', '|')
    #
    #         if isinstance(value, (dict, list)):
    #             clean_data[key] = fix_invalid_keys(value)
    #         else:
    #             clean_data[key] = value
    #
    #     return clean_data
    #
    # elif isinstance(data, list):
    #     clean_data = []
    #     for item in data:
    #         if isinstance(item, dict):
    #             clean_data.append(fix_invalid_keys(item))
    #         else:
    #             clean_data.append(item)
    #
    #     return clean_data
    #
    # else:
    #     raise TypeError("Data must be a dictionary or a list of dictionaries.")
def replace_invalid_keys(data):
    """Replaces invalid characters in the keys of the given data dict or list of dicts.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with invalid characters replaced in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = key.replace('.', '_').replace(' ', '_').replace('/', '|').replace('@', '#')
            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_invalid_keys(value)
            else:
                new_data[new_key] = value

        return new_data

    elif isinstance(data, list):
        new_data = []
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_invalid_keys(item))
            else:
                new_data.append(item)

        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


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
        - fixing invalid keys in the data.
        - Converting the data to newline delimited json.

    Args:
        data (dict, list[dict]): The data to normalize.

    Returns:
        dict, list[dict]: The normalized data.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    logging.info("Normalizing data for BigQuery...")

    # fix invalid keys in the data
    clean_data = replace_invalid_keys(data)

    # convert to newline delimited json
    bq_data = parse_to_nldjson(clean_data, upload_date=True)

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
