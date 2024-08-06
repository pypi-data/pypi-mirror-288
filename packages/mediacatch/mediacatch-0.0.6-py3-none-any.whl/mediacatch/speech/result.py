import json
import logging
import time
from pprint import pprint
from typing import Any

import requests

logger = logging.getLogger('mediacatch.speech.result')


def wait_for_result(
    file_id: str,
    url: str = 'https://s2t.mediacatch.io/api/v2',
    timeout: int = 3600,
    delay: int = 10,
) -> dict[str, Any] | None:
    """Wait for result from a URL.

    Args:
        file_id (str): The file ID to get the result from.
        url (str): The URL to get the result from.
        timeout (int, optional): Timeout for waiting in seconds. Defaults to 3600.
        delay (int, optional): Delay between each request. Defaults to 10.

    Returns:
        dict[str, Any] | None: Dictionary with the result from the URL or None if failed.
    """
    result_url = f'{url}/result/{file_id}'
    logger.info(f'Waiting for result from {result_url}')
    start_time = time.time()
    end_time = start_time + timeout
    while time.time() < end_time:
        try:
            response = requests.get(result_url)
            if response.status_code in [404, 500]:
                pprint(response.json())
                return None

            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(f'Got result from {result_url} in {elapsed_time:.2f} seconds')
            return result

        except (requests.RequestException, json.JSONDecodeError):
            time.sleep(delay)

        except Exception as e:
            logger.error(f'Failed to get result from {result_url}: {e}')
            return None

    logger.error(f'Timeout waiting for result from {result_url}, give up')
    return None
