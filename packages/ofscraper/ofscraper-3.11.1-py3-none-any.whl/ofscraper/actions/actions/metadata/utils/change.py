import asyncio
import pathlib
import random
from functools import partial

import ofscraper.classes.placeholder as placeholder
import ofscraper.actions.utils.general as common
import ofscraper.actions.utils.globals as common_globals
import ofscraper.actions.utils.paths.media as media
import ofscraper.utils.args.accessors.read as read_args
import ofscraper.utils.cache as cache
import ofscraper.utils.hash as hash
import ofscraper.utils.settings as settings
from ofscraper.db.operations_.media import (
    download_media_update,
    prev_download_media_data,
)
from ofscraper.actions.utils.log import get_medialog
from ofscraper.actions.utils.retries import get_download_retries
from ofscraper.actions.utils.params import get_alt_params
from ofscraper.classes.sessionmanager.sessionmanager import (
    FORCED_NEW,SIGN
)
import ofscraper.utils.constants as constants





async def change_metadata(c, ele, username, model_id, placeholderObj=None):
    common_globals.log.info(
        f"{get_medialog(ele)} skipping adding download to disk because metadata is on"
    )
    placeholderObj = placeholderObj or await placeholderObjHelper(c, ele)
    await placeholderObj.init()
    common.add_additional_data(placeholderObj, ele)
    effected = None
    if ele.id:
        prevData = (
            await prev_download_media_data(ele, model_id=model_id, username=username)
            or {}
        )
        await download_media_update(
            ele,
            filename=metadata_file_helper(placeholderObj, prevData),
            directory=metadata_dir_helper(placeholderObj, prevData),
            model_id=model_id,
            username=username,
            downloaded=metadata_downloaded_helper(placeholderObj, prevData),
            hashdata=metadata_hash_helper(placeholderObj, prevData, ele),
            size=metadata_size_helper(placeholderObj, prevData),
        )
        effected = prevData != await prev_download_media_data(
            ele, model_id=model_id, username=username
        )
    return (
        (ele.mediatype if effected else "forced_skipped"),
        0,
    )


def metadata_downloaded_helper(placeholderObj, prevData):
    if read_args.retriveArgs().metadata == "check":
        return prevData["downloaded"] if prevData else None
    elif read_args.retriveArgs().metadata == "complete":
        return 1
    # for update
    elif pathlib.Path(placeholderObj.trunicated_filepath).exists():
        return 1
    elif pathlib.Path(prevData.get("filename") or "").is_file():
        return 1
    elif pathlib.Path(
        prevData.get("directory") or "", prevData.get("filename") or ""
    ).is_file():
        return 1
    return 0


def metadata_file_helper(placeholderObj, prevData):
    if read_args.retriveArgs().metadata != "update":
        return str(placeholderObj.trunicated_filename)
    # for update
    elif pathlib.Path(placeholderObj.trunicated_filepath).exists():
        return str(placeholderObj.trunicated_filename)
    elif pathlib.Path(prevData.get("filename") or "").is_file():
        return prevData.get("filename")
    elif pathlib.Path(
        prevData.get("directory") or "", prevData.get("filename") or ""
    ).is_file():
        return pathlib.Path(
            prevData.get("directory") or "", prevData.get("filename") or ""
        )
    return str(placeholderObj.trunicated_filename)


def metadata_dir_helper(placeholderObj, prevData):
    if read_args.retriveArgs().metadata != "update":
        return str(placeholderObj.trunicated_filedir)
    # for update
    elif pathlib.Path(placeholderObj.trunicated_filedir).exists():
        return str(placeholderObj.trunicated_filedir)
    elif pathlib.Path(prevData.get("directory") or "").is_dir():
        return prevData.get("directory")
    elif pathlib.Path(
        prevData.get("directory") or "", prevData.get("filename") or ""
    ).is_file():
        return pathlib.Path(
            prevData.get("directory") or "", prevData.get("filename") or ""
        ).parent
    return str(placeholderObj.trunicated_filedir)


def metadata_hash_helper(placeholderObj, prevData, ele):
    if not settings.get_hash(mediatype=ele.mediatype):
        return prevData.get("hash")
    elif pathlib.Path(placeholderObj.trunicated_filepath).is_file():
        return hash.get_hash(
            pathlib.Path(placeholderObj.trunicated_filepath), mediatype=ele.mediatype
        )
    elif pathlib.Path(
        prevData.get("directory") or "", prevData.get("filename") or ""
    ).is_file():
        return hash.get_hash(
            pathlib.Path(
                prevData.get("directory") or "", prevData.get("filename") or ""
            )
        )


def metadata_size_helper(placeholderObj, prevData):
    if placeholderObj.size:
        return placeholderObj.size
    elif pathlib.Path(
        prevData.get("directory") or "", prevData.get("filename") or ""
    ).is_file():
        return (
            pathlib.Path(
                prevData.get("directory") or "", prevData.get("filename") or ""
            )
            .stat()
            .st_size
        )
    else:
        return prevData.get("size")


async def metadata_helper(c, ele):
    placeholderObj = None
    if not ele.url and not ele.mpd:
        placeholderObj = placeholder.Placeholders(
            ele, ext=media.content_type_missing(ele)
        )
        return placeholderObj
    else:
        url = ele.url or ele.mpd
        params = get_alt_params(ele) if ele.mpd else None   
        actions=[FORCED_NEW,SIGN] if ele.mpd and constants.getattr("ALT_FORCE_KEY") else []
        common_globals.attempt.set(common_globals.attempt.get() + 1)
        common_globals.log.debug(
            f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{get_download_retries()}]  Getting data for metadata insert"
        )
        async with c.requests_async(
            url=url,
            headers=None,
            params=params,
            actions=actions
        ) as r:
            headers = r.headers
            content_type = headers.get("content-type").split("/")[
                -1
            ] or media.content_type_missing(ele)
            #request fail if not read
            async for _ in r.iter_chunked(20000):
                pass
            placeholderObj = placeholder.Placeholders(
            ele, ext=content_type
            )
            return placeholderObj


async def placeholderObjHelper(c, ele):
    download_data = await asyncio.get_event_loop().run_in_executor(
        common_globals.thread, partial(cache.get, f"{ele.id}_headers")
    )
    if download_data:
        content_type = download_data.get("content-type").split("/")[
            -1
        ] or media.content_type_missing(ele)
        return placeholder.Placeholders(ele, content_type)
    # final fallback
    return await metadata_helper(c, ele)
