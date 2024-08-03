r"""
                                                             
 _______  _______         _______  _______  _______  _______  _______  _______  _______ 
(  ___  )(  ____ \       (  ____ \(  ____ \(  ____ )(  ___  )(  ____ )(  ____ \(  ____ )
| (   ) || (    \/       | (    \/| (    \/| (    )|| (   ) || (    )|| (    \/| (    )|
| |   | || (__     _____ | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
| |   | ||  __)   (_____)(_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
| |   | || (                   ) || |      | (\ (   | (   ) || (      | (      | (\ (   
| (___) || )             /\____) || (____/\| ) \ \__| )   ( || )      | (____/\| ) \ \__
(_______)|/              \_______)(_______/|/   \__/|/     \||/       (_______/|/   \__/
                                                                                      
"""

import asyncio
import pathlib
import re
import traceback

import aiofiles
import psutil
from humanfriendly import format_size

import ofscraper.classes.placeholder as placeholder
import ofscraper.actions.utils.globals as common_globals
import ofscraper.utils.constants as constants
import ofscraper.utils.live.updater as progress_updater
from ofscraper.classes.download_retries import download_retry
from ofscraper.actions.actions.download.utils.alt.attempt import alt_attempt_get
from ofscraper.actions.actions.download.utils.alt.handlers import (
    fresh_data_handler_alt,
    resume_data_handler_alt,
)
from ofscraper.actions.actions.download.utils.alt.item import (
    media_item_keys_alt,
    media_item_post_process_alt,
)
from ofscraper.actions.utils.params import get_alt_params
from ofscraper.actions.utils.log import get_medialog

from ofscraper.actions.actions.download.utils.check.forced import (
    check_forced_skip

)

from ofscraper.actions.actions.download.utils.check.space import (
    downloadspace

)

from ofscraper.actions.actions.download.utils.check.size import (
    size_checker

)
from ofscraper.actions.actions.download.utils.handle_result import handle_result_alt
from ofscraper.actions.utils.log import (
    get_url_log,
    path_to_file_logger,
    temp_file_logger,
)
from ofscraper.actions.actions.download.utils.progress.chunk import (
    get_ideal_chunk_size,
)
from ofscraper.actions.utils.retries import get_download_retries
from ofscraper.actions.utils.send.chunk import send_chunk_msg
from ofscraper.actions.actions.download.utils.total import total_change_helper
from ofscraper.actions.actions.download.utils.resume.resume import get_resume_header, get_resume_size
from ofscraper.actions.actions.download.utils.alt.cache.resume import set_data,get_data
from ofscraper.classes.sessionmanager.sessionmanager import (
    FORCED_NEW,
    SIGN,
)
import ofscraper.utils.auth.request as auth_requests

async def alt_download(c, ele, username, model_id):
    common_globals.log.debug(
        f"{get_medialog(ele)} Downloading with protected media downloader"
    )
    async for _ in download_retry():
        with _:
            try:
                sharedPlaceholderObj = await placeholder.Placeholders(ele, "mp4").init()
                common_globals.log.debug(
                    f"{get_medialog(ele)} download url:  {get_url_log(ele)}"
                )
            except Exception as e:
                raise e

    audio=await ele.mpd_audio
    video=await ele.mpd_video
    path_to_file_logger(sharedPlaceholderObj, ele)

    audio = await alt_download_downloader(audio, c, ele)
    video = await alt_download_downloader(video, c, ele)

    post_result = await media_item_post_process_alt(
        audio, video, ele, username, model_id
    )
    if post_result:
        return post_result
    await media_item_keys_alt(c, audio, video, ele)

    return await handle_result_alt(
        sharedPlaceholderObj, ele, audio, video, username, model_id
    )


async def alt_download_downloader(item, c, ele):
    downloadspace(mediatype=ele.mediatype)
    placeholderObj = await placeholder.tempFilePlaceholder(
        ele, f"{item['name']}.part"
    ).init()
    item["path"] = placeholderObj.tempfilepath
    item["total"] = None
    async for _ in download_retry():
        with _:
            try:
                _attempt = alt_attempt_get(item)
                _attempt.set(_attempt.get(0) + 1)
                if _attempt.get() > 1:
                    pathlib.Path(placeholderObj.tempfilepath).unlink(missing_ok=True)
                data = await get_data(ele,item)
                status = False
                if data:
                    item, status = await resume_data_handler_alt(
                        data, item, ele, placeholderObj
                    )

                else:
                    item, status = await fresh_data_handler_alt(
                        item, ele, placeholderObj
                    )
                if not status:
                    try:
                        item = await alt_download_sendreq(item, c, ele, placeholderObj)
                    except Exception as E:
                        raise E
                return item
            except OSError as E:
                common_globals.log.debug(
                    f"{get_medialog(ele)} [attempt {_attempt.get()}/{get_download_retries()}] Number of Open Files -> { len(psutil.Process().open_files())}"
                )
                common_globals.log.debug(
                    f" {get_medialog(ele)} [attempt {_attempt.get()}/{get_download_retries()}] Open Files -> {list(map(lambda x:(x.path,x.fd),psutil.Process().open_files()))}"
                )
                raise E
            except Exception as E:
                common_globals.log.traceback_(
                    f"{get_medialog(ele)} [attempt {_attempt.get()}/{get_download_retries()}] {traceback.format_exc()}"
                )
                common_globals.log.traceback_(
                    f"{get_medialog(ele)} [attempt {_attempt.get()}/{get_download_retries()}] {E}"
                )
                raise E


async def alt_download_sendreq(item, c, ele, placeholderObj):
    try:
        _attempt = alt_attempt_get(item)
        base_url = re.sub("[0-9a-z]*\.mpd$", "", ele.mpd, re.IGNORECASE)
        url = f"{base_url}{item['origname']}"
        common_globals.log.debug(
            f"{get_medialog(ele)} Attempting to download media {item['origname']} with {url}"
        )
        common_globals.log.debug(
            f"{get_medialog(ele)} [attempt {_attempt.get()}/{get_download_retries()}] download temp path {placeholderObj.tempfilepath}"
        )
        return await send_req_inner(c, ele, item, placeholderObj)
    except OSError as E:
        raise E
    except Exception as E:
        raise E


async def send_req_inner(c, ele, item, placeholderObj):
    total = None
    try:

        resume_size = get_resume_size(placeholderObj, mediatype=ele.mediatype)
        headers = get_resume_header(resume_size, item["total"])
        common_globals.log.debug(f"{get_medialog(ele)} resume header {headers}")
        params = get_alt_params(ele)
        base_url = re.sub("[0-9a-z]*\.mpd$", "", ele.mpd, re.IGNORECASE)
        url = f"{base_url}{item['origname']}"
        headers={"Cookie":f"{ele.hls_header}{auth_requests.get_cookies_str()}"}
        common_globals.log.debug(
            f"{get_medialog(ele)} [attempt {alt_attempt_get(item).get()}/{get_download_retries()}] Downloading media with url  {ele.mpd}"
        )
        async with c.requests_async(
            url=url,
            headers=headers,
            params=params,
            # action=[FORCED_NEW,SIGN] if constants.getattr("ALT_FORCE_KEY") else None

        ) as l:
            item["total"] = int(l.headers.get("content-length"))
            total = item["total"]

            data = {
                "content-total": total,
                "content-type": l.headers.get("content-type"),
            }

            common_globals.log.debug(f"{get_medialog(ele)} data from request {data}")
            common_globals.log.debug(
                f"{get_medialog(ele)} total from request {format_size(data.get('content-total')) if data.get('content-total') else 'unknown'}"
            )
            await total_change_helper(None, total)
            await set_data(ele,item,data)

            temp_file_logger(placeholderObj, ele)
            if await check_forced_skip(ele, total) == 0:
                item["total"] = 0
                total = item["total"]
                await total_change_helper(total, 0)
                return item
            elif total != resume_size:
                await download_fileobject_writer(total, l, ele, placeholderObj,item) 

        await size_checker(placeholderObj.tempfilepath, ele, total)
        return item
    except Exception as E:
        await total_change_helper(total, 0) if total else None
        raise E


async def download_fileobject_writer(total, l, ele, placeholderObj,item):
    common_globals.log.debug(
                    f"{get_medialog(ele)} [attempt {alt_attempt_get(item).get()}/{get_download_retries()}] writing media to disk"
                )
    if total > constants.getattr("MAX_READ_SIZE"):
        await download_fileobject_writer_streamer(total, l, ele, placeholderObj)
    else:
        await download_fileobject_writer_reader(total, l, placeholderObj)
    common_globals.log.debug(
                    f"{get_medialog(ele)} [attempt {alt_attempt_get(item).get()}/{get_download_retries()}] finished writing media to disk"
    )



async def download_fileobject_writer_reader(total, res, placeholderObj):
    pathstr = str(placeholderObj.tempfilepath)

    task1 = progress_updater.add_download_job_task(
        f"{(pathstr[:constants.getattr('PATH_STR_MAX')] + '....') if len(pathstr) > constants.getattr('PATH_STR_MAX') else pathstr}\n",
        total=total,
    )
    fileobject = await aiofiles.open(placeholderObj.tempfilepath, "ab").__aenter__()
    try:
        await fileobject.write(await res.read_())
    except Exception as E:
        raise E
    finally:
        # Close file if needed
        try:
            await fileobject.close()
        except Exception as E:
            raise E
        try:
            progress_updater.remove_download_job_task(task1)
        except Exception as E:
            raise E


async def download_fileobject_writer_streamer(total, res, ele, placeholderObj):

    pathstr = str(placeholderObj.tempfilepath)

    task1 = progress_updater.add_download_job_task(
        f"{(pathstr[:constants.getattr('PATH_STR_MAX')] + '....') if len(pathstr) > constants.getattr('PATH_STR_MAX') else pathstr}\n",
        total=total,
    )
    fileobject = await aiofiles.open(placeholderObj.tempfilepath, "ab").__aenter__()
    download_sleep = constants.getattr("DOWNLOAD_SLEEP")
    chunk_size = get_ideal_chunk_size(total, placeholderObj.tempfilepath)
    try:
        async for chunk in res.iter_chunked(chunk_size):
            await fileobject.write(chunk)
            send_chunk_msg(ele, total, placeholderObj)
            (await asyncio.sleep(download_sleep)) if download_sleep else None
    except Exception as E:
        raise E
    finally:
        # Close file if needed
        try:
            await fileobject.close()
        except Exception as E:
            raise E

        try:
            progress_updater.remove_download_job_task(task1)
        except Exception as E:
            raise E
