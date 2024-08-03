import pathlib

import arrow

import ofscraper.classes.placeholder as placeholder
import ofscraper.actions.utils.general as common
import ofscraper.actions.utils.globals as common_globals
import ofscraper.actions.utils.log as common_logs
import ofscraper.actions.utils.paths.paths as common_paths
import ofscraper.utils.dates as dates
import ofscraper.utils.settings as settings
import ofscraper.utils.system.system as system
from ofscraper.db.operations_.media import download_media_update
from ofscraper.actions.actions.download.utils.check.size import (
    size_checker

)
from ofscraper.utils.system.subprocess  import run


async def handle_result_main(result, ele, username, model_id):
    total, temp, placeholderObj = result
    path_to_file = placeholderObj.trunicated_filepath
    await size_checker(temp, ele, total)
    common_globals.log.debug(
        f"{common_logs.get_medialog(ele)} {await ele.final_filename} size match target: {total} vs actual: {pathlib.Path(temp).absolute().stat().st_size}"
    )
    common_globals.log.debug(
        f"{common_logs.get_medialog(ele)} renaming {pathlib.Path(temp).absolute()} -> {path_to_file}"
    )
    common_paths.moveHelper(temp, path_to_file, ele)
    (
        common_paths.addGlobalDir(placeholderObj.filedir)
        if system.get_parent_process()
        else common_paths.addLocalDir(placeholderObj.filedir)
    )
    if ele.postdate:
        newDate = dates.convert_local_time(ele.postdate)
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} Attempt to set Date to {arrow.get(newDate).format('YYYY-MM-DD HH:mm')}"
        )
        common_paths.set_time(path_to_file, newDate)
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} Date set to {arrow.get(path_to_file.stat().st_mtime).format('YYYY-MM-DD HH:mm')}"
        )

    if ele.id:
        await download_media_update(
            ele,
            filepath=path_to_file,
            model_id=model_id,
            username=username,
            downloaded=True,
            hashdata=await common.get_hash(path_to_file, mediatype=ele.mediatype),
            size=placeholderObj.size,
        )
    await common.set_profile_cache_helper(ele)
    common.add_additional_data(placeholderObj, ele)

    return ele.mediatype, total


async def handle_result_alt(
    sharedPlaceholderObj, ele, audio, video, username, model_id
):
    tempPlaceholder = await placeholder.tempFilePlaceholder(
        ele, f"temp_{ele.filename}_{ele.id}_{ele.postid}.mp4"
    ).init()
    temp_path = tempPlaceholder.tempfilepath
    temp_path.unlink(missing_ok=True)
    t = run(
        [
            settings.get_ffmpeg(),
            "-i",
            str(video["path"]),
            "-i",
            str(audio["path"]),
            "-c",
            "copy",
            "-movflags",
            "use_metadata_tags",
            str(temp_path),
        ]
    )

    if t.stderr.decode().find("Output") == -1:
        common_globals.log.debug(f"{common_logs.get_medialog(ele)} ffmpeg failed")
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} ffmpeg {t.stderr.decode()}"
        )
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} ffmpeg {t.stdout.decode()}"
        )

    video["path"].unlink(missing_ok=True)
    audio["path"].unlink(missing_ok=True)

    common_globals.log.debug(
        f"Moving intermediate path {temp_path} to {sharedPlaceholderObj.trunicated_filepath}"
    )
    common_paths.moveHelper(temp_path, sharedPlaceholderObj.trunicated_filepath, ele)
    (
        common_paths.addGlobalDir(sharedPlaceholderObj.filedir)
        if system.get_parent_process()
        else common_paths.addLocalDir(sharedPlaceholderObj.filedir)
    )
    if ele.postdate:
        newDate = dates.convert_local_time(ele.postdate)
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} Attempt to set Date to {arrow.get(newDate).format('YYYY-MM-DD HH:mm')}"
        )
        common_paths.set_time(sharedPlaceholderObj.trunicated_filepath, newDate)
        common_globals.log.debug(
            f"{common_logs.get_medialog(ele)} Date set to {arrow.get(sharedPlaceholderObj.trunicated_filepath.stat().st_mtime).format('YYYY-MM-DD HH:mm')}"
        )
    if ele.id:
        await download_media_update(
            ele,
            filepath=sharedPlaceholderObj.trunicated_filepath,
            model_id=model_id,
            username=username,
            downloaded=True,
            hashdata=await common.get_hash(
                sharedPlaceholderObj, mediatype=ele.mediatype
            ),
            size=sharedPlaceholderObj.size,
        )
    common.add_additional_data(sharedPlaceholderObj, ele)
    return ele.mediatype, video["total"] + audio["total"]
