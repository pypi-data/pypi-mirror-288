from humanfriendly import format_size

import ofscraper.classes.placeholder as placeholder
import ofscraper.actions.utils.globals as common_globals
from ofscraper.actions.actions.download.utils.check.forced import (
    check_forced_skip

)
from ofscraper.actions.utils.log import path_to_file_logger,get_medialog
from ofscraper.actions.actions.download.utils.resume.resume import get_resume_size,resume_cleaner
from ofscraper.actions.utils.retries import get_download_retries
from ofscraper.actions.actions.download.utils.total import (
    batch_total_change_helper,
    total_change_helper,
)


async def fresh_data_handler_main(ele, tempholderObj):
    common_globals.log.debug(
        f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{get_download_retries()}] fresh download for media {ele.url}"
    )
    resume_size = get_resume_size(tempholderObj, mediatype=ele.mediatype)
    common_globals.log.debug(f"{get_medialog(ele)} resume_size: {resume_size}")


async def resume_data_handler_main(data, ele, tempholderObj, batch=False):
    common_globals.log.debug(
        f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{get_download_retries()}] using data for possible download resumption"
    )
    common_globals.log.debug(f"{get_medialog(ele)} Data from cache{data}")
    common_globals.log.debug(
        f"{get_medialog(ele)} Total size from cache {format_size(data.get('content-total')) if data.get('content-total') else 'unknown'}"
    )

    content_type = data.get("content-type").split("/")[-1]
    total = int(data.get("content-total")) if data.get("content-total") else None
    resume_size = get_resume_size(tempholderObj, mediatype=ele.mediatype)
    resume_size=resume_cleaner(resume_size,total,tempholderObj.tempfilepath)

    common_globals.log.debug(
        f"{get_medialog(ele)} resume_size: {resume_size}  and total: {total}"
    )
    placeholderObj = await placeholder.Placeholders(ele, content_type).init()

    # other
    check = None
    if await check_forced_skip(ele, total) == 0:
        path_to_file_logger(placeholderObj, ele, common_globals.log)
        check = True
    elif total == resume_size:
        common_globals.log.debug(
            f"{get_medialog(ele)} total==resume_size skipping download"
        )
        path_to_file_logger(placeholderObj, ele, common_globals.log)
        if common_globals.attempt.get() == 0:
            pass
        elif not batch:
            total_change_helper(None, total)
        elif batch:
            await batch_total_change_helper(None, total)
        check = True
    return total, placeholderObj, check
