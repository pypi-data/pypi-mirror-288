import json
import logging
from typing import Literal

import requests

from mediacatch import mediacatch_api_key

logger = logging.getLogger('mediacatch.vision.upload')

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-KEY': f'{mediacatch_api_key}',
}


def upload(
    fpath: str,
    type: Literal['ocr', 'face'],
    url: str = 'https://api.mediacatch.io/vision',
    fps: int | None = None,
    tolerance: int | None = None,
    min_bbox_iou: float | None = None,
    min_levenshtein_ratio: float | None = None,
    moving_threshold: int | None = None,
    max_text_length: int | None = None,
    min_text_confidence: float | None = None,
    max_text_confidence: float | None = None,
    max_height_width_ratio: float | None = None,
    get_detection_histogram: bool | None = None,
    detection_histogram_bins: int | None = None,
) -> str:
    """Upload a file to MediaCatch Vision API.

    Args:
        fpath (str): File path.
        type (Literal['ocr', 'face']): Type of inference to run on the file.
        url (str, optional): URL to the vision API. Defaults to 'https://api.mediacatch.io/vision'.
        fps (int, optional): Frames per second for video processing. Defaults to 1.
        tolerance (int, optional): Tolerance for text detection. Defaults to 10.
        min_bbox_iou (float, optional): Minimum bounding box intersection over union for merging text detection. Defaults to 0.5.
        min_levenshtein_ratio (float, optional): Minimum Levenshtein ratio for merging text detection (more info here: https://rapidfuzz.github.io/Levenshtein/levenshtein.html#ratio). Defaults to 0.75.
        moving_threshold (int, optional): If merged text detections center moves more pixels than this threshold, it will be considered moving text. Defaults to 50.
        max_text_length (int, optional): If text length is less than this value, use max_text_confidence as confidence threshold. Defaults to 3.
        min_text_confidence (float, optional): Confidence threshold for text detection (if text length is greater than max_text_length). Defaults to 0.5.
        max_text_confidence (float, optional): Confidence threshold for text detection (if text length is less than max_text_length). Defaults to 0.8.
        max_height_width_ratio (float, optional): Discard detection if height/width ratio is greater than this value. Defaults to 2.0.
        get_detection_histogram (bool, optional): If true, get histogram of detection. Defaults to False.
        detection_histogram_bins (int, optional): Number of bins for histogram calculation. Defaults to 8.

    Returns:
        str: File ID.
    """
    logger.info(f'Uploading file {fpath} to MediaCatch Vision API')

    extra = {}
    if fps is not None:
        extra['fps'] = fps
    if tolerance is not None:
        extra['tolerance'] = tolerance
    if min_bbox_iou is not None:
        extra['min_bbox_iou'] = min_bbox_iou
    if min_levenshtein_ratio is not None:
        extra['min_levenshtein_ratio'] = min_levenshtein_ratio
    if moving_threshold is not None:
        extra['moving_text_threshold'] = moving_threshold
    if max_text_length is not None:
        extra['max_text_length'] = max_text_length
    if min_text_confidence is not None:
        extra['min_text_confidence'] = min_text_confidence
    if max_text_confidence is not None:
        extra['max_text_confidence'] = max_text_confidence
    if max_height_width_ratio is not None:
        extra['max_height_width_ratio'] = max_height_width_ratio
    if get_detection_histogram is not None:
        extra['get_detection_histogram'] = get_detection_histogram
    if detection_histogram_bins is not None:
        extra['detection_histogram_bins'] = detection_histogram_bins

    # Get presigned URL
    data = {'filename': fpath, 'type': type, 'extra': extra}
    response = requests.post(f'{url}/upload/', headers=headers, data=json.dumps(data))
    assert (
        response.status_code == 201
    ), f'Failed to upload file {fpath} to MediaCatch Vision API: {response.text}'
    response_data = response.json()
    file_id = response_data['file_id']

    # Upload file to storage
    with open(fpath, 'rb') as f:
        files = {'file': (response_data['fields']['key'], f)}
        response = requests.post(response_data['url'], data=response_data['fields'], files=files)

    # Mark file as uploaded
    data = {'file_id': file_id}
    response = requests.post(f'{url}/upload/complete/', headers=headers, data=json.dumps(data))
    assert response.status_code == 200, f'Failed to mark file {fpath} as uploaded: {response}'

    logger.info(f'File {fpath} uploaded with ID {file_id}')
    return file_id
