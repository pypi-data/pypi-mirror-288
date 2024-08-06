import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BufferedReader
from pathlib import Path
from typing import Generator

import requests

from mediacatch import mediacatch_api_key

logger = logging.getLogger('mediacatch.speech.upload')


def upload(
    fpath: str | Path,
    quota: str | None = None,
    fallback_language: str | None = None,
    max_threads: int = 5,
    max_request_retries: int = 3,
    request_delay: float = 0.5,
    chunk_size=100 * 1024 * 1024,  # 100 MB
    url: str = 'https://s2t.mediacatch.io/api/v2',
) -> str:
    if not isinstance(fpath, Path):
        fpath = Path(fpath)

    assert fpath.is_file(), f'File {fpath} does not exist'

    logger.info(f'Uploading file {fpath} to MediaCatch Speech API')

    headers = {
        'Content-type': 'application/json',
        'X-API-KEY': mediacatch_api_key,
        'X-Quota': str(quota),
    }

    # Initiate file upload
    start_upload_url = f'{url}/upload/'
    data = {
        'file_name': fpath.name,
        'file_extension': fpath.suffix,
        'quota': quota,
        'fallback_language': fallback_language,
    }
    response = make_request(
        'post',
        start_upload_url,
        headers=headers,
        max_retries=max_request_retries,
        delay=request_delay,
        json=data,
    )
    file_id = response.json()['file_id']

    # Upload file chunks
    upload_file_url = f'{url}/upload/{{file_id}}/{{part_number}}'
    etags = []

    def upload_chunk(part_number: int, chunk: bytes) -> None:
        # Get signed URL to upload chunk
        signed_url_response = make_request(
            'get',
            upload_file_url.format(file_id=file_id, part_number=part_number),
            headers=headers,
        )
        signed_url = signed_url_response.json()['url']

        # Upload chunk to storage
        reponse = requests.put(signed_url, data=chunk)
        etag = reponse.headers['ETag']
        etags.append({'e_tag': etag, 'part_number': part_number})

    with (
        ThreadPoolExecutor(max_workers=max_threads) as executor,
        fpath.open('rb') as f,
    ):
        futures = {
            executor.submit(upload_chunk, part_number, chunk): part_number
            for part_number, chunk in enumerate(
                read_file_in_chunks(file_=f, chunk_size=chunk_size), start=1
            )
        }

        for future in as_completed(futures):
            part_number = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f'Chunk {part_number} failed to upload due to: {e}')

    # Complete file upload
    complete_upload_url = f'{url}/upload/{file_id}/complete'
    response = make_request('post', complete_upload_url, json={'parts': etags}, headers=headers)
    estimated_processing_time = response.json()['estimated_processing_time']

    logger.info(
        f'File {fpath} uploaded successfully. Estimated processing time: {estimated_processing_time}'
    )
    return file_id


def make_request(
    method: str,
    url: str,
    headers: dict[str, str],
    max_retries: int = 3,
    delay: float = 0.5,
    **kwargs,
) -> requests.Response:
    for _ in range(max_retries):
        response = getattr(requests, method)(url, headers=headers, **kwargs)
        if 200 <= response.status_code < 300:
            return response

        if method == 'post' and response.status_code >= 400:
            raise RuntimeError(f'Error during request to {url}', response.json()['detail'])

        time.sleep(delay)

    raise RuntimeError('Maximum retry limit reached for request', None)


def read_file_in_chunks(
    file_: BufferedReader, chunk_size: int = 100 * 1024 * 1024
) -> Generator[bytes, None, None]:
    while chunk := file_.read(chunk_size):
        yield chunk
