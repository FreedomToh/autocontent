import logging
import uuid

from django.conf import settings
from django.core.cache import cache

from api.models import get_notloaded_requests, RequestsModel, add_audio_link_to_request, set_request_audio_loaded
from ggl_service.apis.google_drive import GoogleDriveApi


def get_audio_info(request_obj: RequestsModel) -> dict:
    request_id = request_obj.request_id
    logging.info(f"audio_from_redis start for {request_id}")

    cache_key = f"{settings.TTS_PREFIX}_{request_id}"
    # check, if object exists
    if cache_key not in cache:
        logging.error(f"audio_from_redis fail: No bytes data for {cache_key}")
        return {"error": "no data"}
    return {
        "file_name": f"{uuid.uuid4()}.mp3",
        "cache_key": cache_key
    }


def free_cache(data_info: dict):
    cache_key = data_info.get("cache_key")
    if not cache_key:
        return False
    cache.delete(cache_key)


def load_audio_wrapper():
    logging.info("Start load_audio_wrapper")

    google_api = GoogleDriveApi()

    # get requests, where ready tts, but isn`t loaded to ggl
    requests = get_notloaded_requests()
    for request in requests:
        data_info = get_audio_info(request.request_id)
        if "error" in data_info:
            continue
        result = google_api.load_to_disc(data_info)
        if "url" not in result:
            continue

        if not add_audio_link_to_request(request.request_id, result.get("url")):
            logging.warning(f"load_audio_wrapper for {request.request_id.request_id} fail")
            continue

        set_request_audio_loaded(request)
        free_cache(data_info)
        logging.info(f"load_audio_wrapper for {request.request_id.request_id} finished")

    logging.info("Finished iteration of load_audio_wrapper")

