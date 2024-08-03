import logging

import ofscraper.models.selector as selector
import ofscraper.utils.args.accessors.areas as areas
import ofscraper.utils.constants as constants
import ofscraper.utils.live.updater as progress_updater
import ofscraper.utils.live.tasks as progress_tasks

from ofscraper.commands.utils.strings import (
    area_str,
    avatar_str,
    data_str,
    progress_str,
)

log = logging.getLogger("shared")


def data_helper(user):
    avatar = user.avatar
    username = user.name
    active = user.active
    final_post_areas = areas.get_final_posts_area()
    length = selector.get_num_selected()
    count = progress_tasks.get_user_task_obj().completed

    logging.getLogger("shared_other").warning(
        progress_str.format(count=count + 1, length=length)
    )
    logging.getLogger("shared_other").warning(data_str.format(name=username))
    if constants.getattr("SHOW_AVATAR") and avatar:
        logging.getLogger("shared_other").warning(avatar_str.format(avatar=avatar))
    progress_updater.update_activity_task(
        description=area_str.format(
            areas=",".join(final_post_areas), name=username, active=active
        )
    )
    logging.getLogger("shared_other").info(
        area_str.format(areas=",".join(final_post_areas), name=username, active=active)
    )
