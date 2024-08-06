import json
import os
import logging
from importlib.resources import files

import requests

logger = logging.getLogger('mediacatch.utils.general')


def get_data_from_url(url: str) -> dict:
    """Get data from a URL.

    Args:
        url (str): The URL to get data from.

    Returns:
        dict: Data dictionary from url.
    """
    logger.info(f'Getting data from {url}')
    response = requests.get(url)
    assert response.status_code == 200, f'Failed to get data from {url}: {response}'
    return response.json()


def load_data_from_json(json_file: str) -> dict:
    """Load data from a JSON file.

    Args:
        json_file (str): JSON file with data.

    Returns:
        dict: Data dictionary from JSON file.
    """
    logger.info(f'Loading data from {json_file}')
    assert os.path.isfile(json_file), f'File {json_file} does not exist'
    with open(json_file, 'r') as f:
        result = json.load(f)
    return result


def get_assets_data(fname: str) -> str:
    """Get data from assets folder.

    Args:
        fname (str): File name in assets folder.

    Returns:
        str: _description_
    """
    data_file = files('mediacatch').joinpath(f'assets/{fname}')
    assert data_file.is_file(), f'File {fname} does not exist in mediacatch/assets folder'
    return data_file
